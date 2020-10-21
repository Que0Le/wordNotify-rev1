import { autoinject } from 'aurelia-framework';
import { PLATFORM } from 'aurelia-pal';
import { RouterConfiguration, Router } from "aurelia-router";

@autoinject()
export class ExampleParentRoute {
  message: string;

  constructor(private router: Router) {
    this.message = 'ParentRoute';
  }

  activate() {
    console.log("TCL: ParentRoute -> activate -> activate")
    // this.router.navigate('example-child-route')
  }

  configureRouter(config: RouterConfiguration, router: Router) {
    config.map([
      { route: '', redirect: 'example-child-route' },
      { route: 'example-child-route', name: 'childRoute', nav: true, moduleId: PLATFORM.moduleName('../example-child-route/example-child-route') },
    ])
    this.router = router
  }
}
