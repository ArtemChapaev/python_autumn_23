import time
import weakref
from memory_profiler import profile

from different_classes import Thing, Backpack, SlotsBackpack, WeakrefBackpack


def create_things():
    return [Thing()] * 6


@profile
def test_speed_of_create_backpack(cls, count, passport, lenses, keys, charger, laptop, napkins):
    if count < 0:
        return

    timestamp1 = time.time()

    result = [cls(passport, lenses, keys, charger, laptop, napkins)
              for _ in range(count)]

    timestamp2 = time.time()
    return {'time': timestamp2 - timestamp1, 'res': result}


def test_different_classes_creation(count, pack):
    usual_backpacks = test_speed_of_create_backpack(
        Backpack, count, *pack)

    slots_backpacks = test_speed_of_create_backpack(
        SlotsBackpack, count, *pack)

    weakref_backpacks = test_speed_of_create_backpack(
        WeakrefBackpack, count, *pack)

    print(f"For usual class create of {count} objects: {usual_backpacks['time']}")
    print(f"For class with slots create of {count} objects: {slots_backpacks['time']}")
    print(f"For class with weak references create of {count} objects: {weakref_backpacks['time']}")

    return usual_backpacks['res'], slots_backpacks['res'], weakref_backpacks['res']


@profile
def test_speed_of_swap_values_of_backpack(backpacks, new_pack):
    if isinstance(backpacks[0], WeakrefBackpack):
        timestamp1 = time.time()
        for backpack in backpacks:
            backpack.passport = weakref.ref(new_pack[0])
            backpack.lenses = weakref.ref(new_pack[1])
            backpack.keys = weakref.ref(new_pack[2])
            backpack.charger = weakref.ref(new_pack[3])
            backpack.laptop = weakref.ref(new_pack[4])
            backpack.napkins = weakref.ref(new_pack[5])

        timestamp2 = time.time()
    else:
        timestamp1 = time.time()
        for backpack in backpacks:
            backpack.passport = new_pack[0]
            backpack.lenses = new_pack[1]
            backpack.keys = new_pack[2]
            backpack.charger = new_pack[3]
            backpack.laptop = new_pack[4]
            backpack.napkins = new_pack[5]

        timestamp2 = time.time()

    return {'time': timestamp2 - timestamp1, 'res': backpacks}


def test_different_classes_values_swap(usual_backpacks, slots_backpacks, weakref_backpacks, new_pack):
    usual_count = len(usual_backpacks)
    slots_count = len(usual_backpacks)
    weakref_count = len(usual_backpacks)

    usual_backpack_swapped = test_speed_of_swap_values_of_backpack(
        usual_backpacks, *new_pack)

    slots_backpack_swapped = test_speed_of_swap_values_of_backpack(
        slots_backpacks, *new_pack)

    weakref_backpack_swapped = test_speed_of_swap_values_of_backpack(
        weakref_backpacks, *new_pack)

    print()
    print(f"For usual class swap values of {usual_count} objects: {usual_backpack_swapped['time']}")
    print(f"For class with slots swap values of {slots_count} objects: {slots_backpack_swapped['time']}")
    print(f"For class with weak references swap values of {weakref_count}",
          f"objects: {weakref_backpack_swapped['time']}")


if __name__ == '__main__':
    N = 10 ** 8

    pack_1 = create_things()
    usual_objs, slots_objs, weakref_objs = test_different_classes_creation(N, pack_1)

    pack_2 = create_things()
    test_different_classes_values_swap(usual_objs, slots_objs, weakref_objs, pack_2)
