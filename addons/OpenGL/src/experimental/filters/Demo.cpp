#include <experimental/filters/Demo.h>
#include <experimental/Compositor.h>
#include <roxlu/core/Log.h>

namespace gl { 

  bool DemoFilter::setup(int w, int h) { 

    if(!shader.create(DEMO_FILTER_VS, DEMO_FILTER_FS)) {
      RX_ERROR(ERR_GL_DEMO_SHADER);
      return false;
    }

    shader.bindAttribLocation("a_pos", 0);
    shader.bindAttribLocation("a_tex", 1);

    if(!shader.link()) {
      RX_ERROR(ERR_GL_DEMO_SHADER);
      return false;
    }

    u_tex = shader.getUniformLocation("u_tex");
    return true;
  }

  void DemoFilter::render() { 

    shader.use();

    glDrawBuffer(output.attachment);

    glActiveTexture(GL_TEXTURE0);
    glBindTexture(GL_TEXTURE_2D, input.texture);
    glUniform1i(u_tex, 0);

  }

} // gl

