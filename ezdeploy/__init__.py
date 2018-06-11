# -*- coding: utf-8 -*-
import sys
import importlib

# specify enviroment
try:
    from ezdeploy.env import ENV
    cf = importlib.import_module('ezdeploy.cf_' + ENV)
    sys.modules['ezdeploy.cf'] = sys.modules['ezdeploy.cf_' + ENV]
except ImportError:
    import ezdeploy.cf_production as cf
