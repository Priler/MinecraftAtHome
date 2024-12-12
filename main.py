from ursina import *
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.first_person_controller import FirstPersonController

game = Ursina()

# textures
textures = {
    "grass": {
        # "sides": 'textures/grass_side_carried.png',
        "sides": 'textures/grass_side_carried.png',
        "top": 'textures/grass_carried.png',
        "bottom": 'textures/dirt.png'
    },
}

# shaders config
# lit_with_shadows_shader.default_input['shadow_blur'] = 0
lit_with_shadows_shader.default_input['shadow_color'] = color.rgba(0, 0, 0, 0.1)
game.render.set_depth_offset(0)


class MinecraftHand(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Arm base
        self.arm = Entity(
            parent=self,
            model = 'assets/arm',
            texture='assets/arm_texture.png',
            rotation=Vec3(155, -15, 0),
            position=Vec2(0.6, -0.6),
            scale=0.2
        )

        # Subtle swaying animation
        self.bob_amplitude = 0.005
        self.bob_frequency = 4

    def active(self):
        self.arm.position = Vec2(0.55, -0.55)

    def passive(self):
        self.arm.position = Vec2(0.6, -0.6)

    def update(self):
        # Simple bobbing effect when moving
        t = time.time() * self.bob_frequency
        self.arm.rotation_z += sin(t) * self.bob_amplitude * 10
        self.arm.rotation_x += cos(t) * self.bob_amplitude * 5

        if held_keys['left mouse'] or held_keys['right mouse']:
            hand.active()
        else:
            hand.passive()


# Grass Block
def create_cube(position=(0, 0, 0), cube_type = "grass"):
    # Create parent entity to group cube faces
    cube = Entity(parent = scene, origin_y=.5, highlight_color=color.lime, y = 1, scale = 1, collider = "box", shader = lit_with_shadows_shader)
    cube.position = position

    if cube_type == "grass":
        faces_config = [
            ((0, 0, 0.5), (0, 0, 0), textures["grass"]["sides"]),      # Front
            ((0, 0, -0.5), (0, 180, 0), textures["grass"]["sides"]),    # Back
            ((0.5, 0, 0), (0, 90, 0), textures["grass"]["sides"]),    # Right
            ((-0.5, 0, 0), (0, -90, 0), textures["grass"]["sides"]),   # Left
            ((0, 0.5, 0), (90, 0, 0), textures["grass"]["top"]),      # Top
            ((0, -0.5, 0), (-90, 0, 0), textures["grass"]["bottom"])  # Bottom
        ]
    elif cube_type == "dirt":
        faces_config = [
            ((0, 0, 0.5), (0, 0, 0), textures["grass"]["bottom"]),      # Front
            ((0, 0, -0.5), (0, 180, 0), textures["grass"]["bottom"]),    # Back
            ((0.5, 0, 0), (0, 90, 0), textures["grass"]["bottom"]),    # Right
            ((-0.5, 0, 0), (0, -90, 0), textures["grass"]["bottom"]),   # Left
            ((0, 0.5, 0), (90, 0, 0), textures["grass"]["bottom"]),      # Top
            ((0, -0.5, 0), (-90, 0, 0), textures["grass"]["bottom"])  # Bottom
        ]

    for pos, rot, tex_path in faces_config:
        face = Entity(
            parent=cube,
            model='quad',
            texture=tex_path,
            position=pos,
            rotation=rot,
            double_sided=True,  # Makes both sides of the quad visible
            render_queue=1      # Ensures consistent rendering
        )

    return cube

# Spawn base cubes
for z in range(10):
    for x in range(10):
        grass_block = create_cube(position=(x, 0, z), cube_type="grass")

# grass_cube.animate("rotation_y", grass_cube.rotation_y+360, duration=2, curve=curve.in_out_expo)

# floor
#Entity(model='plane', texture="grass", scale=10, color=color.gray, shader=lit_with_shadows_shader)

# свет (направленный)
directional_light_pivot = Entity()
directional_light = DirectionalLight(parent=directional_light_pivot, shadows=True, rotation=(45, -45, 45), shadow_map_resolution = Vec2(8192, 8192))
directional_light.look_at(Vec3(-1,-1,-0.5))
AmbientLight(color = color.rgba(100, 100, 100, 0.1), intensity = 0.5)

# input
def input(key):
    if key == 'left mouse down' and mouse.hovered_entity:
        if mouse.normal:
            new_position = mouse.hovered_entity.position + mouse.normal
            create_cube(position=new_position, cube_type="dirt")

    if key == 'right mouse down' and mouse.hovered_entity:
        destroy(mouse.hovered_entity)

    if key == 'escape':
        quit()

# player
player = FirstPersonController(y=2, origin_y=-.5)

# Add Minecraft-style hand
hand = MinecraftHand(parent=camera.ui)

# BG color
window.color = color.rgb(141,164,205)

# go go go
game.run() # запускаем будущего конкурента майнкрафту xD