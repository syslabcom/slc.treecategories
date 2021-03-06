from Products.Archetypes import Widget
from Products.Archetypes.Registry import registerWidget
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.ZCatalog.CatalogBrains import AbstractCatalogBrain
from slc.treecategories.interfaces import IInlineTreeView
from zope.component import getMultiAdapter
from zope.interface import implements

class InlineTreeWidget(Widget.InAndOutWidget):
    _properties = Widget.InAndOutWidget._properties.copy()
    _properties.update({'macro' : 'at_widget_inlinetree'})

registerWidget(InlineTreeWidget,
               title='Inline Tree',
               description=('Renders a widget with selected items '
                            'Allows selection of more items via pop up'),
               used_for=('Products.Archetypes.Field.LinesField',)
               )

def getInlineTreeView(context, brain, request, field):
    retval = getMultiAdapter((context, request), name='slc.treecategories.inlinetreeview')
    retval.brain = brain
    #Oh man, could have kept the code as it was...
    retval.realob = brain.getObject()
    retval.context_url = brain.getURL()
    retval._field = field
    return retval

class InlineTreeView(BrowserView):
    implements(IInlineTreeView)

    @property
    def items(self):
        try:
            return self.field.get(self.realob)
        except AttributeError:
            return ("Field '%s' not in brain" % self.field.__name__, )

    @property
    def field(self):
        return self._field

    @property
    def fieldName(self):
        return self.field.getName()
    @property
    def widget(self):
        return self.field.widget

    #property
    def portal(self):
        return self.context
    errors = {}

    render = ViewPageTemplateFile("../browser/inlinetree.pt")
