/*

  # Perlin

  Perlin noise, thanks to Ken P. 
  This class is based on: http://www.flipcode.com/archives/Perlin_Noise_Class.shtml 
  with some super tiny changes. Thanks guys!

  octaves: use a value between 1 - 16, 1 = smooth, 16 = noisy, values between 4 - 8 give conventional noise results
  freq:    use a value between 1 - 8, which will give reasanoble results (you can use any value you want)
  ampl:    a value of 1, will result in values between -1 and 1
  seed:    random seed, eg. 94

 */
#ifndef ROXLU_PERLIN_H
#define ROXLU_PERLIN_H

#include <stdlib.h>
#include <roxlu/math/Vec2.h>
#include <roxlu/math/Vec3.h>

#define PERLIN_SIZE 1024

using namespace roxlu ;

class Perlin {
 public:
  Perlin(int octaves, float freq, float amp, int seed);
  

  float get(float x);
  float get(float x, float y);
  float get(Vec2& v);

 private:
  void initPerlin(int n, float p);
  void init();
  float noise1(float arg);
  float noise2(float vec[2]);
  float noise3(float vec[3]);
  void normalize2(float v[2]);
  void normalize3(float v[3]);
  float noise2D(float vec[2]);

 private:
  int octaves;
  float freq;
  float amp;
  int seed;

  int p[PERLIN_SIZE + PERLIN_SIZE + 2];
  float g3[PERLIN_SIZE + PERLIN_SIZE + 2][3];
  float g2[PERLIN_SIZE + PERLIN_SIZE + 2][2];
  float g1[PERLIN_SIZE + PERLIN_SIZE + 2];
  bool start;
  
};

inline float Perlin::get(float x) {
  float vec[2] = {x, 0.0f};
  return noise2D(vec);
}

inline float Perlin::get(float x, float y) {
  float vec[2] = {x, y};
  return noise2D(vec);
}

inline float Perlin::get(Vec2& v) {
  float vec[2] = { v.x, v.y };
  return noise2D(vec);
}

#endif
