import { PLATFORM } from 'aurelia-pal';

import { RouterConfiguration, Router, RouterEvent } from 'aurelia-router';

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
        moduleId: PLATFORM.moduleName('./router-distributor/router-distributor')
      },
      // Universal routing, aims to add route and links in the view with minimum setup
      {
        route: 'r/*viewModelName',
        moduleId: PLATFORM.moduleName('./router-distributor/router-distributor')
      },
      {
        route: 'example-parent-route',
        title: 'Parent route',
        nav: true,
        moduleId: './pages/examples/example-parent-route/example-parent-route',
      },
    ]);
    this.router = router;
  }
}
