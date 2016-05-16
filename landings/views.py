from random import choice
# Import the register function.
from django.db.models import Q
from django.views.generic import TemplateView
from siteblocks.siteblocksapp import register_dynamic_block
import datetime

from digest.models import Item


def get_active_items():
    return Item.objects.filter(status='active',
                               activated_at__lte=datetime.datetime.now())


def items_preset(items, max_cnt=20):
    return items.prefetch_related('issue', 'section').order_by(
        '-created_at', '-related_to_date')[:max_cnt]


def get_items_by_name(items, name):
    filters = Q(title__icontains=name) | \
              Q(description__icontains=name) | \
              Q(tags__name__in=[name])
    return items.filter(filters)


class DjangoPage(TemplateView):
    template_name = 'landings/pages/django.html'

    def get_context_data(self, **kwargs):
        context = super(DjangoPage, self).get_context_data(**kwargs)
        context['active_menu_item'] = 'feed'
        context['items'] = items_preset(
            get_items_by_name(get_active_items(), 'django'), 10)
        return context


# The following function will be used as a block contents producer.
def get_quote(**kwargs):
    quotes = [  # From Terry Pratchett's Discworld novels.
        'Ripples of paradox spread out across the sea of causality.',
        'Early to rise, early to bed, makes a man healthy, wealthy and dead.',
        'Granny had nothing against fortune-telling provided it was done badly by people with no talent for it.',
        'Take it from me, there\'s nothing more terrible than someone out to do the world a favour.',
        'The duke had a mind that ticked like a clock and, like a clock, it regularly went cuckoo.',
        'Most gods find it hard to walk and think at the same time.',
        'They didn\'t have to be funny - they were father jokes',
        'Speak softly and employ a huge man with a crowbar.',
    ]
    return choice(quotes)


# And we register our siteblock.
register_dynamic_block('my_quotes2', get_quote)
