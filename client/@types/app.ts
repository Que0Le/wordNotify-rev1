import { Router } from "aurelia-router";

export interface IAppRouter {
  viewModelName: string
}

declare global {
  type Replace<Base, With> = {
    [K in keyof Base]: K extends keyof With ? With[K] : Base[K]
  }

  type ReplaceRouterOptions<With> = Replace<Router, { options: With }>;
}
