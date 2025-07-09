const path = require('path');
const webpack = require('webpack');
require('dotenv').config({ path: '/home/vithursh/Coding/EazApply/.env' });

const config = {
  entry: './src/main.tsx',
  mode: process.env.NODE_ENV === 'production' ? 'production' : 'development',
  devtool: process.env.NODE_ENV === 'production' ? 'source-map' : 'eval-source-map',
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.css$/,
        use: [
          'style-loader',
          {
            loader: 'css-loader',
            options: {
              importLoaders: 1
            }
          },
          'postcss-loader'
        ],
        exclude: /bootstrap/
      },
      {
        test: /\.(png|svg|jpg|jpeg|gif)$/i,
        type: 'asset/resource',
      }
    ],
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.js', '.css'],
    alias: {
      '@': path.resolve(__dirname, 'src'),
    }
  },
  optimization: {
    moduleIds: 'deterministic',
    runtimeChunk: 'single',
    splitChunks: {
      chunks: 'all',
      maxInitialRequests: 20,
      minSize: 20000,
      cacheGroups: {
        react: {
          test: /[\\/]node_modules[\\/](react|react-dom)[\\/]/,
          name: 'vendor.react',
          chunks: 'all',
          priority: 40
        },
        mui: {
          test: /[\\/]node_modules[\\/]@mui[\\/]/,
          name: 'vendor.mui',
          chunks: 'all',
          priority: 30
        },
        icons: {
          test: /[\\/]node_modules[\\/]@react-icons[\\/]/,
          name: 'vendor.icons',
          chunks: 'all',
          priority: 20
        },
        default: {
          minChunks: 2,
          priority: -20,
          reuseExistingChunk: true
        }
      }
    }
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env.REACT_APP_SUPABASE_URL': JSON.stringify(process.env.REACT_APP_SUPABASE_URL),
      'process.env.REACT_APP_SUPABASE_KEY': JSON.stringify(process.env.REACT_APP_SUPABASE_KEY),
    })
  ],
  output: {
    filename: '[name].[contenthash].js',
    path: path.resolve(__dirname, 'dist'),
    clean: true,
    publicPath: '/'
  }
};

module.exports = config;