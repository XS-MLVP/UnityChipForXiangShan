import contextlib

from xspcomm import XData

__all__ = ['GetMetaParser']


class MetaParser:
    def __init__(self, val=0):
        x = XData(160, XData.InOut)
        x.SetWriteMode(XData.Imme)
        x.value = val
        self.__x__ = x
        self.providers_valid = [x.SubDataRef(140, 1), x.SubDataRef(143, 1)]
        self.providers = [x.SubDataRef(138, 2), x.SubDataRef(141, 2)]
        self.providerResps_ctr = [x.SubDataRef(131, 3), x.SubDataRef(135, 3)]
        self.providerResps_u = [x.SubDataRef(130, 1), x.SubDataRef(134, 1)]
        self.altUsed = [x.SubDataRef(128, 1), x.SubDataRef(129, 1)]
        self.basecnts = [x.SubDataRef(124, 2), x.SubDataRef(126, 2)]
        self.allocates = [x.SubDataRef(116, 4), x.SubDataRef(120, 4)]
        self.sc_preds = [x.SubDataRef(114, 1), x.SubDataRef(115, 1)]
        self.sc_ctrs = (
            [x.SubDataRef(i * 6 + 66, 6) for i in range(4)],
            [x.SubDataRef(i * 6 + 90, 6) for i in range(4)],
        )
        self.use_alt_on_na = [x.SubDataRef(i, 1) for i in range(2)]

    @property
    def value(self):
        return self.__x__.value

    @value.setter
    def value(self, val):
        self.__x__.value = val


def __clear_value__(obj):
    if isinstance(obj, XData):
        obj.value = 0
    elif isinstance(obj, list):
        for e in obj:
            __clear_value__(e)


class GetMetaParser:
    __obj_pool__ = [MetaParser() for _ in range(4)]

    @contextlib.contextmanager
    def __new__(cls, val=0):
        pool = cls.__obj_pool__
        if pool:
            parser = pool.pop()
            parser.value = val
            yield parser
            for name in dir(parser):
                attr = getattr(parser, name)
                if isinstance(attr, (XData, list)):
                    __clear_value__(attr)
            pool.append(parser)
        else:
            assert False, "No more free object for MetaParser"
