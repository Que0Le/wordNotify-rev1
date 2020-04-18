import { IApiResponse } from './../../../@types/api';
import { IDict } from './../../../@types/index.d';
import { endpoints } from './../../common/endpoints';
import { httpClient } from '../../common/http-client';

export class Dicts {
  message: string;
  dicts: IDict[];

  constructor() {
    this.message = 'Dicts';
  }

  async created() {
    const response = await httpClient.fetch(endpoints.dicts.range(1, 5)) as unknown as IApiResponse<IDict[]>
    this.dicts = response.response
  }
}
