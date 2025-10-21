# -*- coding: utf-8 -*-

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class ItemUpdater:
    """Base class for item update strategies"""
    MIN_QUALITY = 0
    MAX_QUALITY = 50

    def __init__(self, item):
        self.item = item

    def update(self):
        """Update item quality and sell_in"""
        self.update_quality()
        self.update_sell_in()
        self.apply_expired_effect()

    def update_quality(self):
        """Override in subclasses for specific quality update logic"""
        pass

    def update_sell_in(self):
        """Decrease sell_in by 1"""
        self.item.sell_in -= 1

    def apply_expired_effect(self):
        """Override in subclasses for post-expiration effects"""
        pass

    def increase_quality(self, amount=1):
        """Safely increase quality without exceeding max"""
        self.item.quality = min(self.item.quality + amount, self.MAX_QUALITY)

    def decrease_quality(self, amount=1):
        """Safely decrease quality without going below min"""
        self.item.quality = max(self.item.quality - amount, self.MIN_QUALITY)

    def set_quality(self, value):
        """Set quality to a specific value within bounds"""
        self.item.quality = value

    def is_expired(self):
        """Check if item has passed its sell by date"""
        return self.item.sell_in < 0


class NormalItemUpdater(ItemUpdater):
    """Standard item that degrades in quality over time"""

    def update_quality(self):
        if self.item.quality > 0:
            self.item.quality -= 1

    def apply_expired_effect(self):
        if self.is_expired():
            if self.item.quality > 0:
                self.item.quality -= 1


class AgedBrieUpdater(ItemUpdater):
    """Aged Brie increases in quality as it ages"""

    def update_quality(self):
        if self.item.quality < 50:
            self.item.quality += 1

    def apply_expired_effect(self):
        if self.is_expired():
            if self.item.quality < 50:
                self.item.quality += 1


class SulfurasUpdater(ItemUpdater):
    """Legendary item that never changes"""

    def update_quality(self):
        pass

    def update_sell_in(self):
        pass

    def apply_expired_effect(self):
        pass


class BackstagePassUpdater(ItemUpdater):
    """Backstage pass increases in value as concert approaches, worthless after"""

    def update_quality(self):
        if self.item.quality < 50:
            self.item.quality += 1

        if self.item.sell_in < 11:
            if self.item.quality < 50:
                self.item.quality += 1

        if self.item.sell_in < 6:
            if self.item.quality < 50:
                self.item.quality += 1

    def apply_expired_effect(self):
        if self.is_expired():
            self.item.quality = 0


class UpdaterFactory:
    """Factory to create the appropriate updater for each item type"""

    @staticmethod
    def create_updater(item):
        if item.name == "Aged Brie":
            return AgedBrieUpdater(item)
        elif item.name == "Sulfuras, Hand of Ragnaros":
            return SulfurasUpdater(item)
        elif item.name == "Backstage passes to a TAFKAL80ETC concert":
            return BackstagePassUpdater(item)
        else:
            return NormalItemUpdater(item)


class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            updater = UpdaterFactory.create_updater(item)
            updater.update()
