import { autoinject } from 'aurelia-framework';
import { PLATFORM } from 'aurelia-pal';
import { httpClient } from './common/http-client';
import { EventAggregator, Subscription } from 'aurelia-event-aggregator';

interface ISourceSetting {
  name: string
  link: string
}

import { RouterConfiguration, Router, RouterEvent } from 'aurelia-router';

import './app.scss'
import { refreshJumpable } from 'components/features/jumpable/jumpable';

@autoinject()
export class App {
  public message: string = 'Learn some Vocabs';

  private router: Router;

  private httpClient = httpClient;

  private subscriptions: Subscription[] = [];

  private constructor(private eventAggregator: EventAggregator) { }

  bind() {
    this.attachEvents();
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
        moduleId: PLATFORM.moduleName('./router-distributor/router-distributor')
      },
      // Universal routing, aims to add route and links in the view with minimum setup
      {
        route: 'r/*viewModelName',
        moduleId: PLATFORM.moduleName('./router-distributor/router-distributor')
      },
    ]);
    this.router = router;
  }

  attachEvents() {
    this.subscriptions.push(
      // https://aurelia.io/docs/routing/configuration#router-events
      this.eventAggregator.subscribe(RouterEvent.Success, (ev) => {
        /** 1. Refresh jumpable after each navigation */
        window.setTimeout(() => {
          console.log("TCL: App -> attachEvents -> refreshJumpable")
          refreshJumpable();
        }, 0);
      })
    );
  }

}
