var webpack = require('webpack');
var path = require('path');
var ManifestPlugin = require('webpack-manifest-plugin');
var ChunkManifestPlugin = require('chunk-manifest-webpack-plugin');

var BUILD_DIR = path.resolve(__dirname, 'static_content/js');
var APP_DIR = path.resolve(__dirname, 'static_content/js/ab');

var debug = process.env.NODE_ENV !== 'production';

var config = {
  entry: ["babel-polyfill", APP_DIR + '/index.jsx'],
  output: {
    path: BUILD_DIR,
    filename: 'bundle.js'
  },
  module : {
    loaders : [
      {
        test : /\.jsx?/,
        include : APP_DIR,
        loader : 'babel-loader',
      },
      {
        test: /\.json$/,
        loader: 'json-loader'
      },
    ],

    rules: [
            {
                test: /\.css$/,
                exclude: /node_modules/,
                use: [
                    {
                        loader: 'style-loader',
                    },
                    {
                        loader: 'css-loader',
                        options: {
                            importLoaders: 1,
                        }
                    },
                    {
                        loader: 'postcss-loader'
                    }
                ]
            }
    ],
  },
  watchOptions : {
    poll: true,
  },
  
  plugins: debug ? [new ManifestPlugin(),
  
  new ChunkManifestPlugin({
    filename: 'chunk-manifest.json',
    manifestVariable: 'webpackManifest'
  })
  ] : [new webpack.optimize.OccurenceOrderPlugin(),
  new webpack.optimize.DedupePlugin(),
  new webpack.optimize.OccurenceOrderPlugin(),
  new webpack.optimize.UglifyJsPlugin(),
  new webpack.optimize.AggressiveMergingPlugin(),
  new webpack.DefinePlugin({
  'process.env': {
      NODE_ENV: JSON.stringify('production')
    }
  }),
  new webpack.optimize.UglifyJsPlugin()
  ],

};

module.exports = config;
