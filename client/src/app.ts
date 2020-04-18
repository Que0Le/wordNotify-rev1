import { RouterConfiguration, Router, RouterEvent } from 'aurelia-router';
import './common/app-modules';
import { appRoutes } from './router-distributor';

import './app.scss'

export class App {
  public message: string = 'Learn some Vocabs';

  private router: Router;

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
    ]);
    this.router = router;
  }
}
