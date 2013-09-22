/* 

--------------------------------------------------------------------------------
      
                                               oooo              
                                               `888              
                oooo d8b  .ooooo.  oooo    ooo  888  oooo  oooo  
                `888""8P d88' `88b  `88b..8P'   888  `888  `888  
                 888     888   888    Y888'     888   888   888  
                 888     888   888  .o8"'88b    888   888   888  
                d888b    `Y8bod8P' o88'   888o o888o  `V88V"V8P' 
                                                                 
                                                  www.roxlu.com
                                             www.apollomedia.nl                                        
              
--------------------------------------------------------------------------------

   OBJ
   ---
  Super basic OBJ file importer. Only support the minimum to 
  import one object, with the position and normal.

  example:

  ````c++
  OBJ obj;
  obj.load("file.obj");

  std::vector<VertexP> vertices;
  obj.copyVertices(vertices);
  ````

*/


#ifndef ROXLU_OPENGL_OBJ_H
#define ROXLU_OPENGL_OBJ_H

#include <sstream>
#include <map>
#include <string>
#include <fstream>
#include <vector>
#include <string.h>                        /* memcpy/memset */
#include <stdlib.h>                        /* atoi */
#include <glr/Vertex.h>
#include <glr/VBO.h>

#define ERR_OBJ_FILE_NOT_FOUND "Could not open the file: `%s`"
#define ERR_OBJ_WRONG_FACE_INDICES "Incorrect number of indices in face: %ld"
#define ERR_OBJ_NO_VERTICES "No vertices loaded from OBJ file."
#define ERR_OBJ_NO_NORMALS "No normals loaded from OBJ file."

namespace gl {

class OBJ {
 public:
  struct TRI { int v, t, n; };
  struct FACE { TRI a, b, c; };
  struct XYZ {  float x, y, z; };
  struct TEXCOORD { float s, t; };

  bool load(std::string filepath, bool datapath = false);

  bool hasNormals();
  bool hasTexCoords();

  template<class T>
    bool copyVertices(T& result);

  void push_back(Vec3 vert, Vec3 norm, Vec2 tc, VBO<VertexP>& vbo);
  void push_back(Vec3 vert, Vec3 norm, Vec2 tc, VBO<VertexNP>& vbo);
  void push_back(Vec3 vert, Vec3 norm, Vec2 tc, std::vector<VertexP>& verts);
  void push_back(Vec3 vert, Vec3 norm, Vec2 tc, std::vector<VertexNP>& verts);
  void push_back(Vec3 vert, Vec3 norm, Vec2 tc, std::vector<VertexNPT>& verts);
  void push_back(Vec3 vert, Vec3 norm, Vec2 tc, std::vector<VertexPT>& verts);

 public:
  std::vector<Vec3> vertices;
  std::vector<Vec3> normals;
  std::vector<Vec2> tex_coords;
  std::vector<OBJ::FACE> faces;
  std::vector<int> indices;
  bool has_texcoords;
  bool has_normals;
};

template<class T>
inline bool OBJ::copyVertices(T& result) {
  for(std::vector<FACE>::iterator it = faces.begin(); it != faces.end(); ++it) {
    FACE& f = *it;
    push_back(vertices[f.a.v], normals[f.a.n], tex_coords[f.a.t], result) ;
    push_back(vertices[f.b.v], normals[f.b.n], tex_coords[f.b.t], result) ;
    push_back(vertices[f.c.v], normals[f.c.n], tex_coords[f.c.t], result) ;
  }
  return true;
}

inline void OBJ::push_back(Vec3 vert, Vec3 norm, Vec2 tc, VBO<VertexP>& vbo) {
  vbo.push_back(VertexP(vert));
}

inline void OBJ::push_back(Vec3 vert, Vec3 norm, Vec2 tc, VBO<VertexNP>& vbo) {
  vbo.push_back(VertexNP(norm, vert));
}

inline void OBJ::push_back(Vec3 vert, Vec3 norm, Vec2 tc, std::vector<VertexP>& verts) {
  verts.push_back(VertexP(vert));
}

inline void OBJ::push_back(Vec3 vert, Vec3 norm, Vec2 tc, std::vector<VertexNP>& verts) {
  verts.push_back(VertexNP(norm, vert));
}

inline void OBJ::push_back(Vec3 vert, Vec3 norm, Vec2 tc, std::vector<VertexNPT>& verts) {
  verts.push_back(VertexNPT(norm, vert, tc));
}

inline void OBJ::push_back(Vec3 vert, Vec3 norm, Vec2 tc, std::vector<VertexPT>& verts) {
  verts.push_back(VertexPT(vert, tc));
}

inline bool OBJ::hasNormals() {
  return has_normals;
}
 
inline bool OBJ::hasTexCoords() {
  return has_texcoords;
}

} // gl
#endif
