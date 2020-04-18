export const endpoints = {
  dicts: {
    /** '/dicts' */
    base: '/dicts',
    /** '/dicts/${dictId}' */
    single: (dictId: number) => `/dicts/${dictId}`,
    /** '/dicts/${startDictId-endDictId}' */
    range: (startDictId: number, endDictId: number) => `/dicts/${startDictId}-${endDictId}`,
    /** '/dicts/random' */
    random: '/dicts/random',

    // WORDS //
    words: (dictId: number) => ({
      /** '/dicts/${dictId}/words' */
      base: '/dicts/${dictId}/words',
      /** '/dicts/${dictId}/words/${wordId}' */
      single: (wordId: number) => `/dicts/${dictId}/words/${wordId}`,
      /** '/dicts/${dictId}/words/${startWordId-endWordId}' */
      range: (startWordId: number, endWordId: number) => `/dicts/${dictId}/words/${startWordId}-${endWordId}`,
      /** '/dicts/${dictId}/words/random' */
      random: `/dicts/${dictId}/words/random`,
    }),
  }
}
