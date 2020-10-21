import { IWordsListRouter } from './../words-list/words-list';
import { endpoints } from './../../common/endpoints';
import { httpClient } from '../../common/http-client';
import { RouterConfiguration, Router } from 'aurelia-router';

import './dicts.scss';
import { IDict } from '../../../@types/dicts.types';

export class Dicts {
  message: string;
  dicts: IDict[];

  private selectedDictId: number = 4;
  private router: Router;

  constructor() {
    this.message = 'Dicts';
  }

  async created() {
    const response = await httpClient.fetch(endpoints.dicts.range(1, 5)) as unknown as IApiResponse<IDict[]>
    this.dicts = response.response
  }

  configureRouter(config: RouterConfiguration, router: Router) {
    config.map([
      { route: '', redirect: String(this.selectedDictId) },
      {
        route: String(this.selectedDictId), name: 'childRoute', nav: true, moduleId: '../words-list/words-list',
        options: {
          selectedDictId: this.selectedDictId
        } as IWordsListRouter,
      },
    ])
    this.router = router
  }
}
