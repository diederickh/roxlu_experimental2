#include <roxlu/math/Perlin.h>

#define PERLIN_B PERLIN_SIZE
#define PERLIN_BM (PERLIN_SIZE - 1)
#define PERLIN_N 0x1000
#define PERLIN_NP 12 /* 2^N */
#define PERLIN_NM 0xFFF

#define PERLIN_CURVE(t)  ( t * t * (3.0f - 2.0f * t) )
#define PERLIN_LERP(t, a, b) ( a + t * (b - a) )

#define PERLIN_SETUP(i, b0, b1, r0, r1) \
  t = vec[i] + PERLIN_N; \
  b0 = ((int)t) & PERLIN_BM; \
  b1 = (b0+1) & PERLIN_BM; \
  r0 = t - (int)t; \
  r1 = r0 - 1.0f;

Perlin::Perlin(int octaves, float freq, float amp, int seed)
  :octaves(octaves)
  ,freq(freq)
  ,amp(amp)
  ,seed(seed)
  ,start(true)
{
}

float Perlin::noise1(float arg) {
  int bx0, bx1;
  float rx0, rx1, sx, t, u , v, vec[1];
  vec[0] = arg;

  if(start) {
    srand(seed);
    start = false;
    init();
  }

  PERLIN_SETUP(0, bx0, bx1, rx0, rx1);
  sx = PERLIN_CURVE(rx0);
  u = rx0 * g1[ p[bx0] ];
  v = rx1 * g1[ p[bx1] ];
  return PERLIN_LERP(sx, u, v);
}

float Perlin::noise2(float vec[2]) {
  int bx0, bx1, by0, by1, b00, b10, b01, b11;
  float rx0, rx1, ry0, ry1, *q, sx, sy, a, b, t, u, v;
  int i, j;

  if(start) {
    srand(seed);
    start = false;
    init();
  }
  
  PERLIN_SETUP(0, bx0, bx1, rx0, rx1);
  PERLIN_SETUP(1, by0, by1, ry0, ry1);

  i = p[bx0];
  j = p[bx1];

  b00 = p[i + by0];
  b10 = p[j + by0];
  b01 = p[i + by1];
  b11 = p[j + by1];
  
  sx = PERLIN_CURVE(rx0);
  sy = PERLIN_CURVE(ry0);

#define at2(rx, ry) (rx * q[0] + ry * q[1])

  q = g2[b00];
  u = at2(rx0, ry0);
  q = g2[b10];
  v = at2(rx1, ry0);
  a = PERLIN_LERP(sx, u, v);

  q = g2[b01];
  u = at2(rx0, ry1);
  q = g2[b11];
  v = at2(rx1, ry1);
  b = PERLIN_LERP(sx, u, v);

  return PERLIN_LERP(sy, a, b);
}

float Perlin::noise3(float vec[3]) {
  int bx0, bx1, by0, by1, bz0, bz1, b00, b10, b01, b11;
  float rx0, rx1, ry0, ry1, rz0, rz1, *q, sy, sz, a, b, c, d, t, u, v;
  int i, j;
  
  if(start) {
    srand(seed);
    start = false;
    init();
  }

  PERLIN_SETUP(0, bx0, bx1, rx0, rx1);
  PERLIN_SETUP(1, by0, by1, ry0, ry1);
  PERLIN_SETUP(2, bz0, bz1, rz0, rz1);

  i = p[bx0];
  j = p[bx1];

  b00 = p[i + by0];
  b10 = p[j + by0];
  b01 = p[i + by1];
  b11 = p[j + by1];

  t  = PERLIN_CURVE(rx0);
  sy = PERLIN_CURVE(ry0);
  sz = PERLIN_CURVE(rz0);

#define at3(rx,ry,rz) ( rx * q[0] + ry * q[1] + rz * q[2] )

  q = g3[b00 + bz0];
  u = at3(rx0,ry0,rz0);
  q = g3[b10 + bz0]; 
  v = at3(rx1,ry0,rz0);
  a = PERLIN_LERP(t, u, v);

  q = g3[b01 + bz0]; 
  u = at3(rx0,ry1,rz0);
  q = g3[b11 + bz0]; 
  v = at3(rx1,ry1,rz0);
  b = PERLIN_LERP(t, u, v);

  c = PERLIN_LERP(sy, a, b);

  q = g3[b00 + bz1]; 
  u = at3(rx0,ry0,rz1);
  q = g3[b10 + bz1]; 
  v = at3(rx1,ry0,rz1);
  a = PERLIN_LERP(t, u, v);

  q = g3[ b01 + bz1 ]; 
  u = at3(rx0,ry1,rz1);
  q = g3[ b11 + bz1 ]; 
  v = at3(rx1,ry1,rz1);
  b = PERLIN_LERP(t, u, v);

  d = PERLIN_LERP(sy, a, b);

  return PERLIN_LERP(sz, c, d);
}

void Perlin::normalize2(float v[2]) {
  float s;

  s = (float)sqrt(v[0] * v[0] + v[1] * v[1]);
  s = 1.0f/s;
  v[0] = v[0] * s;
  v[1] = v[1] * s;
}

void Perlin::normalize3(float v[3]) {
  float s;

  s = (float)sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]);
  s = 1.0f/s;

  v[0] = v[0] * s;
  v[1] = v[1] * s;
  v[2] = v[2] * s;
}

void Perlin::init(void) {
  int i, j, k;

  for(i = 0 ; i < PERLIN_B ; i++) {
    p[i] = i;
    g1[i] = (float)((rand() % (PERLIN_B + PERLIN_B)) - PERLIN_B) / PERLIN_B;

    for(j = 0 ; j < 2 ; j++) {
      g2[i][j] = (float)((rand() % (PERLIN_B + PERLIN_B)) - PERLIN_B) / PERLIN_B;
    }

    normalize2(g2[i]);

    for(j = 0 ; j < 3 ; j++) {
      g3[i][j] = (float)((rand() % (PERLIN_B + PERLIN_B)) - PERLIN_B) / PERLIN_B;
    }

    normalize3(g3[i]);
  }

  while(--i) {
      k = p[i];
      p[i] = p[j = rand() % PERLIN_B];
      p[j] = k;
  }

  for(i = 0 ; i < PERLIN_B + 2 ; i++) {

    p[PERLIN_B + i] = p[i];
    g1[PERLIN_B + i] = g1[i];

    for (j = 0 ; j < 2 ; j++) {
      g2[PERLIN_B + i][j] = g2[i][j];
    }

    for(j = 0 ; j < 3 ; j++){
      g3[PERLIN_B + i][j] = g3[i][j];
    }

  }
}

float Perlin::noise2D(float vec[2]) {

  float result = 0.0f;
  float amplitude = amp;

  vec[0] *= freq;
  vec[1] *= freq;

  for( int i = 0; i < octaves; i++ ) {
      result += noise2(vec) * amplitude;
      vec[0] *= 2.0f;
      vec[1] *= 2.0f;
      amplitude *= 0.5f;
  }

  return result;
}

