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
        return self.bit(181)

    @provided.setter
    def provided(self, value: int):
        mask = ~(1 << 181)
        self.value = (self.value & mask) | (value << 181)

    @property
    def provider(self):
        """The provider property."""
        return self.bits(180, 178)

    @provider.setter
    def provider(self, value):
        mask = ~(0b111 << 178)
        self.value = (self.value & mask) | (value << 178)

    @property
    def altProvided(self):
        """The altProvided property."""
        return self.bit(177)

    @altProvided.setter
    def altProvided(self, value):
        mask = ~(1 << 177)
        self.value = (self.value & mask) | (value << 177)

    @property
    def altProvider(self):
        """The altProvider property."""
        return self.bits(176, 174)

    @altProvider.setter
    def altProvider(self, value):
        mask = ~(0b111 << 174)
        self.value = (self.value & mask) | (value << 174)

    @property
    def altDiffers(self):
        """The altDiffers property."""
        return self.bit(173)

    @altDiffers.setter
    def altDiffers(self, value):
        mask = ~(1 << 173)
        self.value = (self.value & mask) | (value << 173)

    @property
    def providerU(self):
        """The providerU property."""
        return self.bit(172)

    @providerU.setter
    def providerU(self, value):
        mask = ~(1 << 172)
        self.value = (self.value & mask) | (value << 172)

    @property
    def providerCtr(self):
        """The providerCtr property."""
        return self.bits(171, 170)

    @providerCtr.setter
    def providerCtr(self, value):
        mask = ~(0b11 << 170)
        self.value = (self.value & mask) | (value << 170)

    @property
    def altProviderCtr(self):
        """The altProviderCtr property."""
        return self.bits(169, 168)

    @altProviderCtr.setter
    def altProviderCtr(self, value):
        mask = ~(0b11 << 168)
        self.value = (self.value & mask) | (value << 168)

    @property
    def allocate_valid(self):
        """The allocate_valid property."""
        return self.bit(167)

    @allocate_valid.setter
    def allocate_valid(self, value):
        mask = ~(1 << 167)
        self.value = (self.value & mask) | (value << 167)

    @property
    def allocate_bits(self):
        """The allocate_bits property."""
        return self.bits(166, 164)

    @allocate_bits.setter
    def allocate_bits(self, value):
        mask = ~(0b111 << 164)
        self.value = (self.value & mask) | (value << 164)

    @property
    def providerTarget(self):
        """The providerTarget property."""
        return self.bits(163, 114)

    @providerTarget.setter
    def providerTarget(self, value):
        mask = ~(0X3FFFFFFFFFFFF << 114)
        self.value = (self.value & mask) | (value << 114)

    @property
    def altProviderTarget(self):
        """The altProviderTarget property."""
        return self.bits(113, 64)

    @altProviderTarget.setter
    def altProviderTarget(self, value):
        mask = ~(0X3FFFFFFFFFFFF << 64)
        self.value = (self.value & mask) | (value << 64)
