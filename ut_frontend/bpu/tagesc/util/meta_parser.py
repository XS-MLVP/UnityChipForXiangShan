import contextlib

from dut.tage_sc.UT_Tage_SC.xspcomm import XData

__all__ = ['MetaParser']


class __RealMetaParser__:
    def __init__(self, val=0):
        x = XData(78, XData.InOut)
        x.SetWriteMode(XData.Imme)
        x.value = val
        self.__x__ = x
        self.providers_valid = [x.SubDataRef(74, 1), x.SubDataRef(77, 1)]
        self.providers = [x.SubDataRef(72, 2), x.SubDataRef(75, 2)]
        self.providerResps_ctr = [x.SubDataRef(65, 3), x.SubDataRef(69, 3)]
        self.providerResps_u = [x.SubDataRef(64, 1), x.SubDataRef(68, 1)]
        self.altUsed = [x.SubDataRef(62, 1), x.SubDataRef(63, 1)]
        self.basecnts = [x.SubDataRef(58, 2), x.SubDataRef(60, 2)]
        self.allocates = [x.SubDataRef(50, 4), x.SubDataRef(54, 4)]
        self.sc_preds = [x.SubDataRef(48, 1), x.SubDataRef(49, 1)]
        self.sc_ctrs = [
            [x.SubDataRef(i * 6, 6) for i in range(4)],
            [x.SubDataRef(i * 6 + 24, 6) for i in range(4)],
        ]

    @property
    def value(self):
        return self.__x__.value

    @value.setter
    def value(self, val):
        self.__x__.value = val


def __empty_value__(obj):
    if isinstance(obj, XData):
        obj.value = 0
    elif isinstance(obj, list):
        for e in obj:
            __empty_value__(e)


class MetaParser:
    __obj_pool__ = [__RealMetaParser__() for _ in range(4)]

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
                    __empty_value__(attr)
            pool.append(parser)
        else:
            assert False, "No more free object for MetaParser"

