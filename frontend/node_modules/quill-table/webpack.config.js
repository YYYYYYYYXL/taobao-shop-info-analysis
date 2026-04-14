const path = require('path');
const webpack = require('webpack');
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');

module.exports = {
    entry: './src/index.js',
    output: {
        filename: 'quill-table.js',
        library: 'quillTable',
        libraryTarget: 'umd',
        path: path.resolve(__dirname, 'dist')
    },
    externals: {
        quill: 'quill',
    },
    module: {
        rules: [
            {
                test: /\.css$/,
                use: [
                    'style-loader',
                    'css-loader'
                ]
            },
            {
                test: /\.js$/,
                exclude: /(node_modules)/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['es2015'],
                        plugins: [
                            'transform-runtime',
                        ],
                    }
                }
            }
        ]
    },
    plugins: [
        new UglifyJSPlugin({
            compress: {
                warnings: false,
                screw_ie8: true,
                conditionals: true,
                unused: false,
                comparisons: true,
                sequences: true,
                dead_code: true,
                evaluate: true,
                join_vars: true,
                if_return: true
            },
            output: {
                comments: false
            }
        }),
        new webpack.SourceMapDevToolPlugin({
            filename: 'quill-table.js.map',
        }),
    ]
};
