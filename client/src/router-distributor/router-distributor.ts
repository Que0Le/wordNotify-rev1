import { PLATFORM } from 'aurelia-pal';
import { SettingsPage } from '../pages/settings-page/settings-page';

interface IComponentRoute {
  parentDir: string  // FIX_ME: I don't always want to specify this extra
  module: string
}

export class RouterDistributor {
  message: string;
  viewModelName: string;
  viewModel: string;

  constructor() {
    this.message = 'RouterDistributor';
  }

  /**
   * Add all your pages here, to have them automatically appear in the navigation view
   */
  parentRouteMap = new Map<string, IComponentRoute>([
    ['settings-page', {
      parentDir: '../pages',
      module: PLATFORM.moduleName('../pages/settings-page/settings-page'),
    }],
    ['dicts', {
      parentDir: '../pages',
      module: PLATFORM.moduleName('../pages/dicts/dicts'),
    }],
    ['json-tree', {
      parentDir: '../common/components',
      module: PLATFORM.moduleName('../common/components/json-tree/json-tree'),
    }],
  ]);

  activate(params) {
    if (params.viewModelName !== undefined) {
      const { viewModelName } = params;

      this.viewModelName = viewModelName;
      this.viewModel = `${this.parentRouteMap.get(viewModelName).parentDir}/${viewModelName}/${viewModelName}`;
    }
  }

}
