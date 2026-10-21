// svgo 3.3.2: keep the title, viewBox, role/aria and the candidate comment; 1-decimal precision.
module.exports = {
  multipass: true,
  floatPrecision: 1,
  plugins: [
    {
      name: "preset-default",
      params: {
        overrides: {
          removeTitle: false,
          removeViewBox: false,
          removeComments: false,
          removeUnknownsAndDefaults: { keepRoleAttr: true, keepAriaAttrs: true },
          cleanupIds: false,
          // merging the stacked colour layers changes paint order
          mergePaths: false,
          // would inline favicon.svg's light-scheme `path{fill}` as a style
          // attribute, which then beats the prefers-color-scheme: dark rule
          inlineStyles: false,
        },
      },
    },
  ],
};
