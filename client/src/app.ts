import { autoinject } from 'aurelia-framework';
import { Subscription, EventAggregator } from 'aurelia-event-aggregator';
import { RouterConfiguration, Router, RouterEvent } from 'aurelia-router';
import './common/app-modules';
import '../@types/index.types';
import { appRoutes } from './router-distributor';

import './app.scss'
import { refreshJumpable } from 'components/features/jumpable/jumpable';

@autoinject()
export class App {
  public message: string = 'Learn some Vocabs';

  private router: Router;

  private subscriptions: Subscription[] = [];

  private constructor(private eventAggregator: EventAggregator) {
  }

  bind() {
    this.attachEvents();
  }

  attached() {
    this.refreshJumpable()
  }

  detached() {
    this.subscriptions.forEach(sub => sub.dispose());
  }

  configureRouter(config: RouterConfiguration, router: Router) {
    config.map([
      {
        title: 'Router Distributor',
        route: '',
        nav: true,
        moduleId: appRoutes["router-distributor"]
      },
      // Universal routing, aims to add route and links in the view with minimum setup
      {
        route: 'r/*viewModelName',
        moduleId: appRoutes["router-distributor"]
      },
      {
        route: 'example-parent-route',
        title: 'Parent route',
        nav: true,
        moduleId: appRoutes.nav["example-parent-route"]
      },
      {
        route: 'dicts',
        title: 'Dicts',
        nav: true,
        moduleId: appRoutes.nav.dicts
      },
    ]);
    this.router = router;
  }

  refreshJumpable() {
    window.setTimeout(() => {
      refreshJumpable();
      console.log("TCL: App -> refreshJumpable -> refreshJumpable")
    }, 0);
  }

  attachEvents() {
    this.subscriptions.push(
      // https://aurelia.io/docs/routing/configuration#router-events
      this.eventAggregator.subscribe(RouterEvent.Success, this.refreshJumpable)
    );
  }
}
