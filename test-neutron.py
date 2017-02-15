#/usr/local/bin/neutron-server --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/plugins/ml2/ml2_conf.ini --config-file /etc/neutron/plugins/dragonflow.ini

import sys
import os

from oslo_config import cfg
from oslo_db import api as oslo_db_api
from oslo_db import exception as db_exc
from oslo_log import helpers as log_helpers
from sqlalchemy.orm import exc

import oslo_db.sqlalchemy.session
from neutron.db.models import securitygroup as sg_models
from neutron.common import config as common_config
from neutron.api.v2 import attributes
from neutron.db import api as db_api
from neutron.db import common_db_mixin
from neutron import context
from neutron.db.migration.connection import DBConnection

from oslo_log import log as logging
LOG = logging.getLogger(__name__)

_db_opts = [
    cfg.StrOpt('connection',
               default='',
               secret=True,
               help=_('URL to database')),
    cfg.StrOpt('engine',
               default='',
               help=_('Database engine for which script will be generated '
                      'when using offline migration.')),
]

CONF = cfg.ConfigOpts()
#CONF.register_cli_opts(_core_opts)
CONF.register_cli_opts(_db_opts, 'database')


class TestClass(common_db_mixin.CommonDbMixin):
  def __init__(self):
    print("class init")

  def run(self):
    DBConnection(CONF.database.connection)
    tenant_id = '56418eb1bba14ab7bdf6a411663a3821'
    LOG.debug('XXX2 ensure_default_security_group tenant %s', tenant_id)
    ctx = context.get_admin_context()
    with ctx.session.begin(subtransactions=True):
      query = self._model_query(ctx, sg_models.DefaultSecurityGroup)
      f = query.filter_by(tenant_id=tenant_id)
      default_group = f.one()
      LOG.debug('XXX2 res %s', str(default_group))
      print(default_group['security_group_id'])



if __name__ == "__main__":
  common_config.init(['--config-file', '/etc/neutron/neutron.conf'])
  test = TestClass()
  test.run()

