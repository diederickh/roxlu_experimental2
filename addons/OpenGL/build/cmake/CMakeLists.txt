# opengl

roxlu_add_addon(Image)

roxlu_addon_begin("opengl")

  # --------------------------------------------------------------------------------------
  roxlu_addon_add_source_file(glr/Shader.cpp)
  roxlu_addon_add_source_file(glr/Texture.cpp)
  roxlu_addon_add_source_file(glr/VAO.cpp)
  roxlu_addon_add_source_file(glr/Drawer.cpp)
  #roxlu_addon_add_source_file(glr/Font.cpp) # conflicts with OF
  roxlu_addon_add_source_file(glr/Camera.cpp)
  roxlu_addon_add_source_file(glr/FBO.cpp)
  roxlu_addon_add_source_file(io/OBJ.cpp)

  roxlu_addon_add_source_file(experimental/Filter.cpp)
  roxlu_addon_add_source_file(experimental/Compositor.cpp)
  roxlu_addon_add_source_file(experimental/Scene.cpp)
  roxlu_addon_add_source_file(experimental/filters/Demo.cpp)
  roxlu_addon_add_source_file(experimental/filters/VerticalBlur.cpp)
  roxlu_addon_add_source_file(experimental/filters/HorizontalBlur.cpp)
  roxlu_addon_add_source_file(experimental/filters/Luminance.cpp)
  # --------------------------------------------------------------------------------------

roxlu_addon_end()
