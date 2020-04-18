import { IWord } from './../../../@types/dicts.types';
import { endpoints } from './../../common/endpoints';
import { httpClient } from './../../common/http-client';
import { autoinject } from 'aurelia-framework';

export interface IWordsListRouter {
  selectedDictId: number
}

@autoinject()
export class WordsList {
  message: string;

  constructor(private router: ReplaceRouterOptions<IWordsListRouter>) {
    this.message = 'WordsList';
  }

  async activate(_: any, router: ReplaceRouterOptions<IWordsListRouter>) {
    const { selectedDictId } = router.options;
    const response = await httpClient.fetch(endpoints.dicts.words(selectedDictId).range(100, 105)) as unknown as IApiResponse<IWord[]>;
    const words = response.response
    console.log("TCL: WordsList -> activate -> words", words)
  }
}
