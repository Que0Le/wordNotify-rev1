import { autoinject } from 'aurelia-framework';
import { EventAggregator, Subscription } from 'aurelia-event-aggregator';
import { PLATFORM } from 'aurelia-pal';
import { RouterEvent } from 'aurelia-router';
import { refreshJumpable } from 'components/features/jumpable/jumpable';

interface IComponentRoute {
  parentDir: string  // FIX_ME: I don't always want to specify this extra
  module: string
}

@autoinject()
export class RouterDistributor {
  message: string;
  viewModelName: string;
  viewModel: string;

  private constructor(private eventAggregator: EventAggregator) {
    this.message = 'RouterDistributor';
  }

  private subscriptions: Subscription[] = [];

  bind() {
    this.attachEvents();
  }

  attached() {
    this.refreshJumpable()
  }

  detached() {
    this.subscriptions.forEach(sub => sub.dispose());
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
    ['home', {
      parentDir: '../pages',
      module: PLATFORM.moduleName('../pages/home/home'),
    }],
    ['json-tree', {
      parentDir: '../common/components',
      module: PLATFORM.moduleName('../common/components/json-tree/json-tree'),
    }],
  ]);

  activate(params: IAppRouter) {
    if (params.viewModelName !== undefined) {
      const { viewModelName } = params;

      this.viewModelName = viewModelName;
      const viewModelRouteInfo = this.parentRouteMap.get(viewModelName);
      if (viewModelRouteInfo === undefined) throw new Error('No route found');

      this.viewModel = `${viewModelRouteInfo.parentDir}/${viewModelName}/${viewModelName}`;
    }
  }

  refreshJumpable() {
    window.setTimeout(() => {
      refreshJumpable();
    }, 0);
  }

  attachEvents() {
    this.subscriptions.push(
      // https://aurelia.io/docs/routing/configuration#router-events
      this.eventAggregator.subscribe(RouterEvent.Success, this.refreshJumpable)
    );
  }
}
