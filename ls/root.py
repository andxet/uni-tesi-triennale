# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, lurl, request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_

from pheritage.lib.base import BaseController
from pheritage.controllers.error import ErrorController
from pheritage.model.guarini import Locale, Categoria
from pheritage import model
from bson.objectid import ObjectId


c_locale = model.mainsession.db.locali
c_categoria = model.mainsession.db.categorie


__all__ = ['RootController']


class RootController(BaseController):
    """
    The root controller for the pheritage application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """

    error = ErrorController()

    def _before(self, *args, **kw):
        tmpl_context.project_name = "pheritage"

    @expose('pheritage.templates.index')
    def index(self):
        """Handle the front-page."""
        print 'ricevuto'
        return dict(page='index')

    #@expose('pheritage.templates.data')
    @expose('json')
    def data(self, **kw):
        """This method showcases how you can use the same controller for a data page and a display page"""
        return dict(page='data', params=kw)
        
    @expose('json')
    def categories(self):
        cat = c_categoria.find({}, fields={'_id': False})
        return dict(data=list(cat))
        
    @expose('json')
    def cities(self):
        cities = list(c_locale.find().distinct('comune'))
        cities.sort()
        return dict(data=cities)
        
    @expose('json')
    def types(self, city='TORINO'):
        print(city)
        t = {}
        if city != 'TUTTI I COMUNI':
                t['comune'] = city
        types = c_locale.find(t, fields={'_id': False, 'tipo': True}).distinct('tipo')
        try:
            types.remove('')
        except ValueError:
            pass
        types.sort()
        return dict(data=types)

    @expose('json')
    def points(self, **kw):
        t = {}
        try:
            if kw['city'] != 'TUTTI I COMUNI':
                t['comune']= kw['city']
        except KeyError:
            pass
        try:
            if kw['type'] != 'Tutti i tipi':
                t['tipo'] = kw['type']
        except KeyError:
            pass
        print(t)
        points = c_locale.find(t, fields=['lat', 'lon', 'id']).sort('comune')
        return dict(data=list(points))
        #return list(points) //Open to csrf attacks
        
    @expose('json')
    def detail(self, id):
        det = c_locale.find({'_id': ObjectId(id)})
        return dict(data = list(det))