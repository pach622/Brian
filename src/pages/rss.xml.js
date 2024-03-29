import rss from '@astrojs/rss';

export const get = () =>
  rss({
    title: 'Brian\'s portfolio ',
    description: 'Tech and personal writing',
    site: import.meta.env.SITE,
    items: import.meta.glob('./**/*.mdx'),
    customData: `<language>en-us</language>`,
  });
