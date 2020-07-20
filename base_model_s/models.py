from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from tinymce.models import HTMLField


class Category(models.Model):
    """
    Simple model for categorizing entries.
    """

    title = models.CharField(_('Name'), max_length=255)

    description = models.TextField(_('Description'), blank=True)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __str__(self):
        return self.title


class Element(models.Model):
    __doc__ = _("Products and services that the company buys, sells or produces.")

    name = models.CharField(_('Product/Service Name'), max_length=250, db_index=True)
    description = HTMLField(
        _('Long Description'), blank=True, default='',
        help_text=_('Long description for explain to customers the advantages and benefits of the product or service, '
                    'also your especial characteristics.'))
    category = models.ForeignKey(Category, verbose_name=_('Category'), null=True, blank=True)

    kind = models.CharField(_('Kind'), max_length=1, default='1', choices=(
        ('1', _('Product')),
        ('2', _('Service')),
        ('3', _('Fixed Asset')),
    ))

    unity = models.CharField(
        _('Unity of measurement'), max_length=255, default='', blank=True,
        help_text=_('Kilograms, meters, liters, unit, according to the presentation of the product.')
    )

    mark = models.CharField(_('Commercial Brand'), max_length=200, blank=True, default='')
    sku = models.CharField(
        _('Code'), max_length=100, blank=True, default='',
        help_text=_("Bar code or unique code for the product or service"))
    supplier = models.ManyToManyField(
        'User', verbose_name=_('Suppliers'), blank=True,
        help_text=_('Set the suppliers for this product or service, this is used in Purchase Orders')
    )
    cost = models.DecimalField(
        _('Cost'), default='0', blank=True,
        max_digits=20,
        decimal_places=2,
        help_text=_('Purchase price or manufacturing cost. The system updates the cost each time a purchase '
                    'is registered. Calculating the weighted average value among all purchases made of the product. '
                    'This value is used when the expense is caused when selling an inventory product or when making '
                    'inventory exits.')
    )
    agent_price = models.DecimalField(
        _('Price for franchisee'), default=0, blank=True,
        max_digits=20,
        decimal_places=2,
        help_text=_('This price is used in inventory transfers to the branches of another company'))

    sell_price = models.DecimalField(
        _('Sale price'),
        default=0,
        blank=True,
        max_digits=20,
        decimal_places=2,
        help_text=_('Price to which this product/service is sold to your customers'),
    )

    tax_percentage = models.FloatField(
        _('Tax percentage'),
        default=0,
    )

    image = models.ImageField(
        _('Image'), upload_to='element/%Y/', blank=True, default='',
        help_text=_('This image is displayed when you search for the product to add to the invoices. '
                    'It facilitates the identification and minimizes the error when registering the items of '
                    'the invoice')
    )

    active = models.BooleanField(
        _('Enable'), default=True,
        help_text=_("If the product or service is no longer used, do not delete it of the system, better disable it."),
    )

    inventory_control = models.BooleanField(
        _('Inventory control'), blank=True, default=False,
        help_text=_('When you register a purchase and sale invoice, the system will update the inventory, '
                    'if this box is checked.'))

    # taxes = models.ManyToManyField('billing_s.Tax', verbose_name=_('Taxes'), blank=True)

    profit_margin = models.FloatField(
        _('Profit margin %'), default=0, blank=True, null=True,
        help_text=_('(Price - cost) / Price, you can massively update the price of the products based on the defined '
                    'profit margin')
    )

    integration_id = models.CharField(
        _('Integration id'),
        max_length=255,
        help_text=_('Id for integrate with other software'),
        null=True,
        blank=True,
        db_index=True,
    )

    integration_category = models.CharField(
        _('Integration category'),
        max_length=255,
        help_text=_('Category in other software'),
        null=True,
        blank=True,
    )

    objects = models.Manager()

    autocomplete_similar = 'name'

    UNIT_OF_TIME_KEYS = {
        '1': 'seconds',
        '2': 'minutes',
        '3': 'hours',
        '4': 'days',
    }

    class Options:
        create_field = 'name'

    class Meta:
        # unique_together = (('name', 'id_user_isis'),)
        verbose_name = _('Product/Service')
        verbose_name_plural = _('Products/Services')
        permissions = [('view_price_analysis', _('View price analysis'))]
