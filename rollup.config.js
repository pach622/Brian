import image from '@rollup/plugin-image';

export default {
  input: 'src/index.js', // Adjust to your project's entry file
  output: {
    dir: 'dist',
    format: 'es', // Output format (e.g., 'cjs', 'es', etc.)
  },
  plugins: [
    image(), // Add support for images
  ],
  external: [
    '/src/assets/FoodHub/deliveryTimePlotCode.png', // Add problematic file as external
  ],
};