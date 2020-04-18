import { IAppRouter } from './../../@types/app';
import { autoinject } from 'aurelia-framework';
import { EventAggregator, Subscription } from 'aurelia-event-aggregator';
import { RouterEvent } from 'aurelia-router';
import { refreshJumpable } from 'components/features/jumpable/jumpable';

import './router-distributor.scss';

interface IComponentRoute {
  parentDir: string  // FIX_ME: I don't always want to specify this extra
  module: string
}

@autoinject()
export class RouterDistributor {
  viewModelName: string;
  viewModel: string;

  private constructor(private eventAggregator: EventAggregator) {
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
    ['home', {
      parentDir: '../pages',
      module: '../pages/home/home',
    }],
    ['settings-page', {
      parentDir: '../pages',
      module: '../pages/settings-page/settings-page',
    }],
    ['dicts', {
      parentDir: '../pages',
      module: '../pages/dicts/dicts',
    }],
    ['example-parent-route', {
      parentDir: '../pages',
      module: '../pages/examples/example-parent-route/example-parent-route',
    }],
    ['json-tree', {
      parentDir: '../common/components',
      module: '../common/components/json-tree/json-tree',
    }],
  ]);

  hasChildRoutes = [
    'example-parent-route',
  ]

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
