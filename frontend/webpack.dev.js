const { merge } = require("webpack-merge");
const commonConfig = require("./webpack.config");
const { EnvironmentPlugin } = require("webpack");
const { Mode, Api } = require("@mui/icons-material");
require("postcss");

const devConfig = {
    mode: "development",  // Add a comma here
    plugins: [
        new EnvironmentPlugin({
            API: "google.com"
        }),
    ],
};

module.exports = merge(commonConfig, devConfig);