from xspcomm import *

if __name__ == '__main__':
    x = XData(200, XData.InOut)
    x.SetWriteMode(XData.Imme)

    r = x.SubDataRef(90, 6)
    r.SetWriteMode(XData.Imme)
    r.value = 1

    assert r.value == 1
    assert x.value == 0x40000000000000000000000
    pass
