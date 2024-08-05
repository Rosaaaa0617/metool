import meta
from meta import parts
from meta import constants
from meta import models


def main():
    m = models.Model(0)
    part = parts.Part(id=2, type=constants.PSOLID, model_id=m.id)
    prop = part.get_property()
    print(prop)


if __name__ == "__main__":
    main()