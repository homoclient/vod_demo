import numpy as np
import moderngl as mgl
import pyglet
import os
import ctypes
if os.name == 'nt':
  ctypes.windll.user32.SetProcessDPIAware()

adj = np.array([
  [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
  [1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0],
  [1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0],
  [1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0],
  [1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0],
  [1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
  [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1],
  [0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
  [0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1],
  [0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1],
  [0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1],
  [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0]
])
rule_lut = np.r_[0, 0, 0, 1, 1, 1]

rng = np.random.default_rng(seed=0)
# w = rng.choice([0, 1], 12)

w_next = np.vectorize(lambda x: np.packbits(np.hstack([np.zeros(4, dtype=np.uint8), rule_lut[adj@np.unpackbits(np.array([x//256,x%256],dtype=np.uint8))[-12:]]]))@[256,1])(np.arange(2**12))

def draw_state(vao, x, y, w, h, screen_w, screen_h, state):
  scale_x = w/screen_w
  offset_x = 2*x/screen_w + scale_x - 1.0
  scale_y = h/screen_h
  offset_y = 2*y/screen_h + scale_y - 1.0
  transform = np.array([[scale_x, 0, offset_x], [0, scale_y, offset_y], [0, 0, 1]], dtype='f4')
  vao.program['translate'] = transform.flatten('F')
  vao.program['cell_states'] = state
  vao.render()

config = pyglet.gl.Config(sample_buffers=1, samples=4)
window_size = 1920, 1080
window = pyglet.window.Window(*window_size, resizable=False, vsync=False, config=config, fullscreen=True)
ctx = mgl.create_context()
fbo = ctx.screen

dodeca_coords = np.array(
  [-9.51056520e-01,  3.09016990e-01, -5.87785250e-01, -8.09016990e-01,
  0.00000000e+00,  1.00000000e+00,  5.87785250e-01, -8.09016990e-01,
  9.51056520e-01,  3.09016990e-01,  9.51056516e-01,  3.09016994e-01,
  1.90211303e+00,  6.18033989e-01,  1.17557050e+00,  1.61803399e+00,
  0.00000000e+00,  1.00000000e+00,  0.00000000e+00,  2.00000000e+00,
  -5.30568282e-09,  1.00000000e+00, -1.06113656e-08,  2.00000000e+00,
  -1.17557052e+00,  1.61803399e+00, -9.51056520e-01,  3.09016990e-01,
  -1.90211304e+00,  6.18033980e-01, -9.51056511e-01,  3.09016994e-01,
  -1.90211302e+00,  6.18033987e-01, -1.90211302e+00, -6.18033984e-01,
  -5.87785250e-01, -8.09016990e-01, -1.17557050e+00, -1.61803398e+00,
  -5.87785249e-01, -8.09016991e-01, -1.17557050e+00, -1.61803398e+00,
  1.43375973e-09, -1.99999999e+00,  5.87785250e-01, -8.09016990e-01,
  1.17557050e+00, -1.61803398e+00,  5.87785249e-01, -8.09016999e-01,
  1.17557050e+00, -1.61803400e+00,  1.90211303e+00, -6.18034000e-01,
  9.51056520e-01,  3.09016990e-01,  1.90211304e+00,  6.18033980e-01,
  1.90211303e+00,  6.18033989e-01,  1.90211303e+00, -6.18033989e-01,
  2.85316955e+00, -9.27050983e-01,  1.76335576e+00,  2.42705098e+00,
  1.17557050e+00,  1.61803399e+00, -1.06113656e-08,  2.00000000e+00,
  1.17557050e+00,  1.61803400e+00,  1.76335575e+00,  2.42705100e+00,
  -1.76335577e+00,  2.42705098e+00, -1.17557052e+00,  1.61803399e+00,
  -1.90211302e+00,  6.18033987e-01, -1.17557050e+00,  1.61803398e+00,
  -1.76335575e+00,  2.42705097e+00, -2.85316954e+00, -9.27050977e-01,
  -1.90211302e+00, -6.18033984e-01, -1.17557050e+00, -1.61803398e+00,
  -1.90211302e+00, -6.18033987e-01, -2.85316953e+00, -9.27050981e-01,
  2.15063958e-09, -2.99999999e+00,  1.43375973e-09, -1.99999999e+00,
  1.17557050e+00, -1.61803400e+00, -1.06113654e-08, -2.00000000e+00,
  -1.59170480e-08, -3.00000001e+00,  2.85316955e+00, -9.27051000e-01,
  1.90211303e+00, -6.18034000e-01, -3.50000000e+00, -3.50000000e+00,
  3.50000000e+00, -3.50000000e+00,  3.50000000e+00,  3.50000000e+00,
  -3.50000000e+00,  3.50000000e+00, -0.00000000e+00, -3.00000000e+00,
  2.85316956e+00, -9.27050970e-01,  1.76335575e+00,  2.42705097e+00,
  -1.76335575e+00,  2.42705097e+00, -2.85316956e+00, -9.27050970e-01], dtype='f4') * 1/3.5
cell_flags = np.hstack([np.tile(np.array([1,2,4,8,16,32,64,128,256,512,1024], dtype='u4'), [5,1]).flatten('F'), 2048*np.ones(9,dtype='u4')])
dodeca_index = np.array(
  [ 2,  0,  1,  2,  1,  3,  2,  3,  4,  7,  5,  6,  7,  8,  5,  7,  9,
  8, 12, 10, 11, 12, 13, 10, 12, 14, 13, 17, 15, 16, 17, 18, 15, 17,
  19, 18, 22, 20, 21, 22, 23, 20, 22, 24, 23, 27, 25, 26, 27, 28, 25,
  27, 29, 28, 30, 31, 32, 30, 32, 33, 30, 33, 34, 35, 36, 37, 35, 37,
  38, 35, 38, 39, 40, 41, 42, 40, 42, 43, 40, 43, 44, 45, 46, 47, 45,
  47, 48, 45, 48, 49, 50, 51, 52, 50, 52, 53, 50, 53, 54, 55, 59, 63,
  55, 56, 59, 56, 60, 59, 56, 57, 60, 57, 61, 60, 57, 62, 61, 57, 58,
  62, 58, 63, 62, 58, 55, 63], dtype='u4')

prog = ctx.program(
  vertex_shader="""
#version 330
in vec2 in_vert;
in uint in_cell_flag;
out vec3 frag_color;

uniform uint cell_states;
uniform mat3 translate;

void main() {
  gl_Position = vec4((translate*vec3(in_vert, 1.0)).xy, 0.0, 1.0);
  //gl_Position = vec4(in_vert, 0.0, 1.0);
  frag_color = float((in_cell_flag & cell_states) != 0u) * vec3(0.9, 0.9, 0.7) + vec3(0.1, 0.1, 0.2);

}
""",
  fragment_shader="""
#version 330
in vec3 frag_color;
out vec3 f_color;
void main() {
  f_color = frag_color;
}
""")

vbo_vert = ctx.buffer(dodeca_coords.tobytes())
vbo_flag = ctx.buffer(cell_flags.tobytes())
ibo = ctx.buffer(dodeca_index.tobytes())
vao = ctx.vertex_array(prog, [(vbo_vert, '2f4 /v', 'in_vert'), (vbo_flag, 'u4', 'in_cell_flag')], index_buffer=ibo, mode=mgl.TRIANGLES)

w = np.arange(4096)
@window.event
def on_draw():
  window.clear()
  global w
  for i in range(64):
    for j in range(64):
      draw_state(vao, (window_size[0]/64)*i, (window_size[1]/64)*j, window_size[0]/64, window_size[1]/64, *window_size, w[i*64+j])

@window.event
def on_key_press(symbol, modifiers):
  global w
  if symbol == pyglet.window.key.R:
    w = np.arange(4096)
  elif symbol == pyglet.window.key.SPACE:
    w = w_next[w]

pyglet.app.run()