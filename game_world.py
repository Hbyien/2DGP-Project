#world[0] : 백그라운드 객체들, 즉 맨 아래에 그려야할 객체들
#world[1] : 포어그라운들 객체들, 위에 그려야할 객체들
#
import coin
import knight

#world = []#단일계층구조
world = [[] for _ in range(4)]

collision_pairs={}

def add_collision_pair(group,a,b):
    if group not in collision_pairs:
        collision_pairs[group]=[ [] , [] ]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)



def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)

def add_object(o, depth):
    world[depth].append(o)

def render():
    for layer in world:
        for o in layer:
            o.draw()

def update():
    for layer in world:
        for o in layer:
            o.update()



def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            del o
            return
    raise ValueError('Cannot delete non existing object')

def clear():
    for layer in world:
        layer.clear()



def collide(a, b):
    if a == knight.Knight and b== coin.Coin:
        al,ab,ar,at=a.get_bb_top()
    else:
        al, ab, ar, at = a.get_bb()

    bl,bb,br,bt= b.get_bb()


    if ar<bl: return False
    if al>br: return False
    if at<bb: return False
    if ab>bt : return False

    return True # 충돌발생


def collide_top(a, b):

    al,ab,ar,at=a.get_bb_top()
    bl,bb,br,bt= b.get_bb()


    if ar<bl: return False
    if al>br: return False
    if at<bb: return False
    if ab>bt : return False

    return True # 충돌발생
def collide_bottom(a, b):

    al,ab,ar,at=a.get_bb_bottom()
    bl,bb,br,bt= b.get_bb()


    if ar<bl: return False
    if al>br: return False
    if at<bb: return False
    if ab>bt : return False

    return True # 충돌발생

def handle_collisions():
    for group,pairs in collision_pairs.items():
        if group == 'knight_top:qblock':
            for a in pairs[0]:
                for b in pairs[1]:
                    if collide_top(a, b):
                        print(f'{group} collide top')
                        a.handle_collision(group, b)
                        b.handle_collision(group, a)
        if group == 'knight_bottom:qblock':
            for a in pairs[0]:
                for b in pairs[1]:
                    if collide_bottom(a, b):
                        print(f'{group} collide bottom')
                        a.handle_collision(group, b)
                        b.handle_collision(group, a)
        else:
            for a in pairs[0]:
                for b in pairs[1]:
                    if collide(a,b):
                        print(f'{group} collide')
                        a.handle_collision(group,b)
                        b.handle_collision(group,a)






    return None

