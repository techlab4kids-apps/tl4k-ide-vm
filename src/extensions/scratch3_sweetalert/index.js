const ArgumentType = require('../../extension-support/argument-type');
const BlockType = require('../../extension-support/block-type');
const formatMessage = require('format-message');
import Swal from 'sweetalert2';

const DOMPurify  = require('dompurify');

// Source: https://gist.github.com/bgrins/6194623
const isDataUri = function (string) {
    const regex = /^\s*data:([a-z]+\/[a-z+]+(;[a-z\-]+\=[a-z\-]+)?)?(;base64)?,[a-z0-9\!\$\&\'\,\(\)\*\+\,\;\=\-\.\_\~\:\@\/\?\%\s]*\s*$/i;
    return !!string.match(regex);
}

/**
 * Icon svg to be displayed at the left edge of each extension block, encoded as a data URI.
 * @type {string}
 */
// eslint-disable-next-line max-len
const menuIconURI = 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNyAyNSI+PGRlZnM+PHN0eWxlPi5jbHMtMXtmaWxsOm5vbmU7fS5jbHMtMntmaWxsOiNjZTU3NGU7fTwvc3R5bGU+PC9kZWZzPjxnIGlkPSJDYWxxdWVfMiIgZGF0YS1uYW1lPSJDYWxxdWUgMiI+PGcgaWQ9IkxheWVyXzEiIGRhdGEtbmFtZT0iTGF5ZXIgMSI+PHJlY3QgY2xhc3M9ImNscy0xIiB3aWR0aD0iMjciIGhlaWdodD0iMjUiLz48ZyBpZD0iQnJvd3NlciI+PHBhdGggY2xhc3M9ImNscy0yIiBkPSJNMjAsMTguMjNIN2EuNzguNzgsMCwwLDEtLjc4LS43OFY3LjlBMS4xMywxLjEzLDAsMCwxLDcuMzMsNi43N0gxOS42N0ExLjEzLDEuMTMsMCwwLDEsMjAuNzksNy45djkuNTVBLjc4Ljc4LDAsMCwxLDIwLDE4LjIzWk03LjMzLDcuMjlhLjYuNiwwLDAsMC0uNi42MXY5LjU1YS4yNi4yNiwwLDAsMCwuMjYuMjZIMjBhLjI2LjI2LDAsMCwwLC4yNi0uMjZWNy45YS42LjYsMCwwLDAtLjYtLjYxWiIvPjxnIGlkPSJ0b3AiPjxwYXRoIGNsYXNzPSJjbHMtMiIgZD0iTTcuMzMsN0gxOS42N2EuODYuODYsMCwwLDEsLjg2Ljg2VjkuNjVhMCwwLDAsMCwxLDAsMEg2LjQ3YTAsMCwwLDAsMSwwLDBWNy45QS44Ni44NiwwLDAsMSw3LjMzLDdaIi8+PC9nPjwvZz48L2c+PC9nPjwvc3ZnPg==';
const blockIconURI = 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNyAyNSI+PGRlZnM+PHN0eWxlPi5jbHMtMXtmaWxsOm5vbmU7fS5jbHMtMntmaWxsOiNmZmY7fTwvc3R5bGU+PC9kZWZzPjxnIGlkPSJDYWxxdWVfMiIgZGF0YS1uYW1lPSJDYWxxdWUgMiI+PGcgaWQ9IkxheWVyXzEiIGRhdGEtbmFtZT0iTGF5ZXIgMSI+PHJlY3QgY2xhc3M9ImNscy0xIiB3aWR0aD0iMjciIGhlaWdodD0iMjUiLz48cGF0aCBjbGFzcz0iY2xzLTIiIGQ9Ik0xOS42Niw2LjdINy4zM0ExLjEyLDEuMTIsMCwwLDAsNi4yMSw3LjgydjkuNTVhLjc4Ljc4LDAsMCwwLC43OC43OEgyMGEuNzguNzgsMCwwLDAsLjc3LS43OFY3LjgyQTEuMTIsMS4xMiwwLDAsMCwxOS42Niw2LjdaTTIwLDE3LjYzSDdhLjI1LjI1LDAsMCwxLS4yNi0uMjZWOS41N0gyMC4yN3Y3LjhBLjI2LjI2LDAsMCwxLDIwLDE3LjYzWiIvPjwvZz48L2c+PC9zdmc+';

class SweetAlert {
    constructor (runtime) {
        /**
         * The runtime instantiating this block package.
         * @type {Runtime}
         */
        this.runtime = runtime;
    }

    /**
     * @returns {object} metadata for this extension and its blocks.
     */
    getInfo() {
        return {
            id: 'sweetalert2',
            name: 'SweetAlert 2',
            color1: '#0088ff',
            color2: '#0063ba',
            blocks: [
                {
                    opcode: 'alert',
                    blockType: Scratch.BlockType.COMMAND,
                    text: 'alert with text [text] and desc [desc]',
                    arguments: {
                        text: {
                            type: Scratch.ArgumentType.STRING,
                            defaultValue: 'hi',
                        },
                        desc: {
                            type: Scratch.ArgumentType.STRING,
                            defaultValue: 'e',
                        },
                    },
                },
                {
                    opcode: 'alert2',
                    blockType: Scratch.BlockType.COMMAND,
                    text: 'redirect alert with text [text], desc [desc], and url [url]',
                    arguments: {
                        text: {
                            type: Scratch.ArgumentType.STRING,
                            defaultValue: 'hi',
                        },
                        desc: {
                            type: Scratch.ArgumentType.STRING,
                            defaultValue: 'e',
                        },
                        url: {
                            type: Scratch.ArgumentType.STRING,
                            defaultValue: 'https://snail-ide.vercel.app',
                        },
                    },
                },
            ],
        };
        
    }
    alert (args) {
        Swal.fire({
            title: args.text,
            text: args.desc,
            confirmButtonText: "Ok",
            icon: "success",
            allowOutsideClick: true,
        })
    }
    alert2 (args) {
        Swal.fire({
            title: args.text,
            text: args.desc,
            confirmButtonText: "Open page",
            icon: "success",
            allowOutsideClick: true,
            preConfirm: () => {
                window.location.href = this.alert2;
            }
        })
    }

      getMessage(id) {
        return localisation.messages[id][this._locale];
      }
    }

module.exports = Scratch3AdaBrowserBlocks;