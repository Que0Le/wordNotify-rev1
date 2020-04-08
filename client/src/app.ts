import { PLATFORM } from 'aurelia-pal';
interface ISourceSetting {
  name: string
  link: string
}

import { RouterConfiguration, Router } from 'aurelia-router';

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
    ]);
    this.router = router;
  }

}
