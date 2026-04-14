const path = require('path');
const webpack = require('webpack');

module.exports = {
    entry: './src/demo.js',
    output: {
        filename: 'demo.js',
        path: path.resolve(__dirname, 'demo')
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
        new webpack.SourceMapDevToolPlugin({
            filename: 'demo.js.map',
        }),
    ]
};
