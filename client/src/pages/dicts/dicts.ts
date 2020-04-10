import { httpClient } from '../../common/http-client';

export class Dicts {
  message: string;

  constructor() {
    this.message = 'Dicts';
  }

  async created() {
    // const response = await httpClient.fetch('/resources/dicts?dict_db=DE_FR&random=true')
    // console.log("TCL: Dicts -> created -> response", response)
  }
}
