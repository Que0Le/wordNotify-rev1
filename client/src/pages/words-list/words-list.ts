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
  words: IWord[];

  constructor(private router: ReplaceRouterOptions<IWordsListRouter>) {
    this.message = 'WordsList';
  }

  async activate(_: any, router: ReplaceRouterOptions<IWordsListRouter>) {
    const { selectedDictId } = router.options;
    const response = await httpClient.fetch(endpoints.dicts.words(selectedDictId).range(200, 205)) as unknown as IApiResponse<IWord[]>;
    this.words = response.response
    console.log("TCL: WordsList -> activate -> this.words", this.words)
  }
}
