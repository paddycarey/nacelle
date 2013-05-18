# third party imports
from google.appengine.ext import ndb

# third party imports
from wtforms.ext.appengine.ndb import model_form

# local imports
from cms.forms.form import IPSecureForm
from cms.handlers.base import CMSTemplateHandler
from nacelle.utils.stringutils import prettify_string


class CMSBulkActionHandler(CMSTemplateHandler):

    model = None

    def post(self, action):

        action = action.replace('_multi', '')
        entity_ids = self.request.get('ids', ',').split(',')
        completed_actions = []
        for entity_id in entity_ids:
            if not entity_id:
                continue
            getattr(self, action)(entity_id)
            completed_actions.append(entity_id)

        if completed_actions:
            self.session.add_flash('%sd: %s' % (prettify_string(action), ', '.join(completed_actions)))
        return self.response.out.write('Success')

    def get_entity(self, entity_id):
        try:
            entity = self.model.get_by_id(int(entity_id))
        except ValueError:
            entity = self.model.get_by_id(entity_id)
        if entity is None:
            return self.abort(404)
        return entity

    def delete(self, entity_id):
        entity = self.get_entity(entity_id)
        entity.key.delete()


class CMSDeleteHandler(CMSTemplateHandler):

    model = None

    def get(self, key):

        try:
            entity = self.model.get_by_id(int(key))
        except ValueError:
            entity = self.model.get_by_id(key)
        if not entity:
            self.session.add_flash('Unable to delete: %s' % key)
        else:
            self.session.add_flash('Deleted: %s' % key)
            entity.key.delete()
        return self.redirect(self.request.referer)


class CMSFormHandler(CMSTemplateHandler):

    model = None

    def get_model_form(self, key):

        try:
            if key is None and hasattr(self.model.Meta, 'new_form_fields'):
                fields = self.model.Meta.new_form_fields
            else:
                fields = self.model.Meta.form_fields
        except AttributeError:
            fields = None

        if fields is None:
            return model_form(self.model, base_class=IPSecureForm)
        return model_form(self.model, only=[x['property'] for x in fields], field_args=dict([(x['property'], x['args']) for x in fields]), base_class=IPSecureForm)

    def handle(self, key=None):

        mform = self.get_model_form(key)

        if key is not None:
            # get entity from datastore if editing
            try:
                entity = self.model.get_by_id(int(key))
            except ValueError:
                entity = self.model.get_by_id(key)
            if entity is None:
                return self.abort(404, detail="entity not found")
            # build form instance (with POST data if avail)
            form = mform(self.request.POST, obj=entity, csrf_context=self.request.remote_addr + self.get_user().key.id())
            success_url = '../../'
        else:
            # build form instance (with POST data if avail)
            form = mform(self.request.POST, csrf_context=self.request.remote_addr + self.get_user().key.id())
            success_url = '../'
            entity = None

        # check if form was POSTed and that user input validates
        if self.request.method == 'POST' and form.validate():

            # populate object and store
            if key is None:
                # create model if required
                if hasattr(self.model.Meta, 'form_constructor'):
                    constructor = getattr(self.model.Meta, 'form_constructor')
                    entity = getattr(self.model, constructor[0])(**dict([(x, getattr(form, x).data) for x in constructor[1:]]))
                else:
                    entity = self.model()
            form.populate_obj(entity)
            entity.put()
            # add success message to site and redirect to newly created/edited entity
            self.session.add_flash('Updated entity: %s' % str(entity.key.id()))
            return self.redirect(success_url)

        elif form.csrf_token.errors:

            # check if form didnt validate because of a CSRF error
            self.session.add_flash('CSRF Token Error: Entity not saved, try again')

        # get configuration from the specified model
        header_config = {
            'title': self.model.Meta.header_title or 'Manage %ss' % self.model._get_kind(),
            'icon': self.model.Meta.header_icon,
            'text': self.model.Meta.header_text,
        }

        # declare template and context
        _template = 'cms/models/form.html'
        _context = {'form': form, 'entity': entity, 'header_config': header_config, 'success_url': success_url}
        # render response as appropriate
        return self.render_response(_template, _context)


class CMSListTableHandler(CMSTemplateHandler):

    model = None

    def get(self):

        redirect = False
        if 'sort_property' in self.request.GET:
            self.session['%s-sort_property' % self.request.path] = self.request.get('sort_property')
            redirect = True
        if 'sort_order' in self.request.GET:
            self.session['%s-sort_order' % self.request.path] = self.request.get('sort_order')
            redirect = True
        if redirect:
            return self.redirect(self.request.path)

        # get configuration from the specified model
        header_config = {
            'title': self.model.Meta.header_title or 'Manage %ss' % self.model._get_kind(),
            'icon': self.model.Meta.header_icon,
            'text': self.model.Meta.header_text,
        }
        table_config = self.model.Meta.list_columns
        query_config = {
            'sort_property': self.session.get('%s-sort_property' % self.request.path, self.model.Meta.default_sort_property),
            'sort_order': self.session.get('%s-sort_order' % self.request.path, self.model.Meta.default_sort_order),
        }

        # render template and return
        template = self.model.Meta.custom_list_template or 'cms/models/list.html'
        context = {'header_config': header_config, 'table_config': table_config, 'sort_config': query_config}
        return self.render_response(template, context)


class CMSListRowHandler(CMSTemplateHandler):

    model = None

    def get_query(self):

        # build query object
        query = self.model.query()

        # check if sort order
        sort_property = self.request.get('sort_property')
        if not sort_property:
            return self.abort(400, detail='sort_property query param required')

        if not self.request.get('sort_order') == 'desc':
            query = query.order(getattr(self.model, sort_property))
        else:
            query = query.order(-getattr(self.model, sort_property))

        # get page size and cursor
        page_size = int(self.request.get('page_size', default_value=25))
        cursor = self.request.get('cursor', default_value=None)
        if cursor == 'None':
            cursor = None
        if cursor:
            cursor = ndb.Cursor.from_websafe_string(cursor)

        results, cursor, more = query.fetch_page(page_size, start_cursor=cursor, keys_only=True)
        if more:
            cursor = cursor.to_websafe_string()
        else:
            cursor = None
        return ndb.get_multi_async(results), cursor

    def get(self):

        # get query for this handler
        results, cursor = self.get_query()

        # render template and return
        template = self.model.Meta.custom_list_template or 'cms/models/rows.html'
        context = {
            'query': results, 'cursor': cursor,
            'table_config': self.model.Meta.list_columns,
            'action_config': self.model.Meta.list_actions,
            'model_name': self.model._get_kind(),
        }
        return self.render_response(template, context)
