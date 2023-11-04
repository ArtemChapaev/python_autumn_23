import time
import weakref
from memory_profiler import profile

from different_classes import Thing, Backpack, SlotsBackpack, WeakrefBackpack


@profile
def test_speed_of_create_backpack(cls, count, passport, lenses, keys, charger, laptop, napkins):
    timestamp1 = time.time()

    result = [cls(passport, lenses, keys, charger, laptop, napkins)
              for _ in range(count)]

    timestamp2 = time.time()
    return {'time': timestamp2 - timestamp1, 'res': result}


passport1 = Thing()
lenses1 = Thing()
keys1 = Thing()
charger1 = Thing()
laptop1 = Thing()
napkins1 = Thing()

passport2 = Thing()
lenses2 = Thing()
keys2 = Thing()
charger2 = Thing()
laptop2 = Thing()
napkins2 = Thing()

N = 10 ** 8

usual_backpack_created = test_speed_of_create_backpack(
    Backpack, N, passport1, lenses1, keys1, charger1, laptop1, napkins1)

slots_backpack_created = test_speed_of_create_backpack(
    SlotsBackpack, N, passport1, lenses1, keys1, charger1, laptop1, napkins1)

weakref_backpack_created = test_speed_of_create_backpack(
    WeakrefBackpack, N, passport1, lenses1, keys1, charger1, laptop1, napkins1)

print(f"For usual class create of {N} objects: {usual_backpack_created['time']}")
print(f"For class with slots create of {N} objects: {slots_backpack_created['time']}")
print(f"For class with weak references create of {N} objects: {weakref_backpack_created['time']}")


@profile
def test_speed_of_swap_values_of_backpack(
        backpacks, new_passport, new_lenses, new_keys, new_charger, new_laptop, new_napkins):
    if isinstance(backpacks[0], WeakrefBackpack):
        timestamp1 = time.time()
        for backpack in backpacks:
            backpack.passport = weakref.ref(new_passport)
            backpack.lenses = weakref.ref(new_lenses)
            backpack.keys = weakref.ref(new_keys)
            backpack.charger = weakref.ref(new_charger)
            backpack.laptop = weakref.ref(new_laptop)
            backpack.napkins = weakref.ref(new_napkins)

        timestamp2 = time.time()
    else:
        timestamp1 = time.time()
        for backpack in backpacks:
            backpack.passport = new_passport
            backpack.lenses = new_lenses
            backpack.keys = new_keys
            backpack.charger = new_charger
            backpack.laptop = new_laptop
            backpack.napkins = new_napkins

        timestamp2 = time.time()

    return {'time': timestamp2 - timestamp1, 'res': backpacks}


usual_backpack_swapped = test_speed_of_swap_values_of_backpack(
    usual_backpack_created['res'], passport2, lenses2, keys2, charger2, laptop2, napkins2)

slots_backpack_swapped = test_speed_of_swap_values_of_backpack(
    slots_backpack_created['res'], passport2, lenses2, keys2, charger2, laptop2, napkins2)

weakref_backpack_swapped = test_speed_of_swap_values_of_backpack(
    weakref_backpack_created['res'], passport2, lenses2, keys2, charger2, laptop2, napkins2)

print()
print(f"For usual class swap values of {N} objects: {usual_backpack_swapped['time']}")
print(f"For class with slots swap values of {N} objects: {slots_backpack_swapped['time']}")
print(f"For class with weak references swap values of {N}",
      "objects: {weakref_backpack_swapped['time']}")
