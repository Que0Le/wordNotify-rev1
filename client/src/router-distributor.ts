import { IAppRouter } from '../@types/app';
import { autoinject } from 'aurelia-framework';
import { EventAggregator, Subscription } from 'aurelia-event-aggregator';
import { RouterEvent } from 'aurelia-router';
import { refreshJumpable } from 'components/features/jumpable/jumpable';

import './router-distributor.scss';

export const appRoutes = {
  nav: {
    // pages
    'home': './pages/home/home',
    'dicts': './pages/dicts/dicts',

    'example-parent-route': './pages/examples/example-parent-route/example-parent-route',
    'settings-page': './pages/settings-page/settings-page',
    // common
    'json-tree': './common/components/json-tree/json-tree',
  },
  'router-distributor': './router-distributor'
}

@autoinject()
export class RouterDistributor {
  viewModelName: string;
  viewModel: string;

  private constructor(private eventAggregator: EventAggregator) {
  }

  // private subscriptions: Subscription[] = [];

  // bind() {
  //   this.attachEvents();
  // }

  // attached() {
  //   this.refreshJumpable()
  // }

  // detached() {
  //   this.subscriptions.forEach(sub => sub.dispose());
  // }

  /**
   * Add all your pages here, to have them automatically appear in the navigation view
   */
  parentRouteMap = new Map<string, string>(Object.entries(appRoutes.nav));

  hasChildRoutes = [
    'example-parent-route',
    'dicts',
  ]

  activate(params: IAppRouter) {
    if (params.viewModelName !== undefined) {
      const { viewModelName } = params;

      this.viewModelName = viewModelName;
      const viewModelRouteInfo = this.parentRouteMap.get(viewModelName);
      if (viewModelRouteInfo === undefined) throw new Error('No route found');

      this.viewModel = viewModelRouteInfo;
    }
  }

  // refreshJumpable() {
  //   window.setTimeout(() => {
  //     // refreshJumpable();
  //   }, 0);
  // }

  // attachEvents() {
  //   this.subscriptions.push(
  //     // https://aurelia.io/docs/routing/configuration#router-events
  //     // this.eventAggregator.subscribe(RouterEvent.Success, this.refreshJumpable)
  //   );
  // }
}
