__all__ = ['MetaParser']

class MetaParser:
    def __init__(self, meta: int) -> None:
        self.value = meta
        pass

    def bits(self, high, low):
        assert low <= high
        mask = (1 << (high + 1)) - 1
        return (self.value & mask) >> low

    def bit(self, bit):
        return (self.value >> bit) & 1

    @property
    def meta(self) -> int:
        return self.value

    @property
    def provided(self) -> int:
        return self.bit(117)

    @provided.setter
    def provided(self, value: int):
        mask = ~(1 << 117)
        self.value = (self.value & mask) | (value << 117)

    @property
    def provider(self):
        """The provider property."""
        return self.bits(116, 114)

    @provider.setter
    def provider(self, value):
        mask = ~(0b111 << 114)
        self.value = (self.value & mask) | (value << 114)

    @property
    def altProvided(self):
        """The altProvided property."""
        return self.bit(113)

    @altProvided.setter
    def altProvided(self, value):
        mask = ~(1 << 113)
        self.value = (self.value & mask) | (value << 113)

    @property
    def altProvider(self):
        """The altProvider property."""
        return self.bits(112, 110)

    @altProvider.setter
    def altProvider(self, value):
        mask = ~(0b111 << 110)
        self.value = (self.value & mask) | (value << 110)

    @property
    def altDiffers(self):
        """The altDiffers property."""
        return self.bit(109)

    @altDiffers.setter
    def altDiffers(self, value):
        mask = ~(1 << 109)
        self.value = (self.value & mask) | (value << 109)

    @property
    def providerU(self):
        """The providerU property."""
        return self.bit(108)

    @providerU.setter
    def providerU(self, value):
        mask = ~(1 << 108)
        self.value = (self.value & mask) | (value << 108)

    @property
    def providerCtr(self):
        """The providerCtr property."""
        return self.bits(107, 106)

    @providerCtr.setter
    def providerCtr(self, value):
        mask = ~(0b11 << 106)
        self.value = (self.value & mask) | (value << 106)

    @property
    def altProviderCtr(self):
        """The altProviderCtr property."""
        return self.bits(105, 104)

    @altProviderCtr.setter
    def altProviderCtr(self, value):
        mask = ~(0b11 << 104)
        self.value = (self.value & mask) | (value << 104)

    @property
    def allocate_valid(self):
        """The allocate_valid property."""
        return self.bit(103)

    @allocate_valid.setter
    def allocate_valid(self, value):
        mask = ~(1 << 103)
        self.value = (self.value & mask) | (value << 103)

    @property
    def allocate_bits(self):
        """The allocate_bits property."""
        return self.bits(102, 100)

    @allocate_bits.setter
    def allocate_bits(self, value):
        mask = ~(0b111 << 100)
        self.value = (self.value & mask) | (value << 100)

    @property
    def providerTarget(self):
        """The providerTarget property."""
        return self.bits(95, 50)

    @providerTarget.setter
    def providerTarget(self, value):
        mask = ~(0X3FFFFFFFFFFFF << 50)
        self.value = (self.value & mask) | (value << 50)

    @property
    def altProviderTarget(self):
        """The altProviderTarget property."""
        return self.bits(49, 0)

    @altProviderTarget.setter
    def altProviderTarget(self, value):
        mask = ~(0X3FFFFFFFFFFFF << 0)
        self.value = (self.value & mask) | (value << 0)
