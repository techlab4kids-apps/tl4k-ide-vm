const ArgumentType = require('../extension-support/argument-type');
const BlockType = require('../extension-support/block-type');
const formatMessage = require('format-message');
const Swal = require('sweetalert2');
const blockIconURI = "data:image/png;base64,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"

class Sweetalert2ext {
    constructor(runtime) {
        this.runtime = runtime;
        this.buttonPressed = false;  // did you press it?
    }

    getInfo() {
        return {
            id: 'sweetalert2',
            name: 'Sweetalert2',
            blockIconURI: blockIconURI,
            blocks: [
                // this is very silly

                {
                    opcode: 'showCustomSweetAlert',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'coreExample.showCustomSweetAlert',
                        default: 'Show Custom SweetAlert2 with options: Title [title], Message [message], Icon [icon], Confirm Text [confirmText]',
                        description: 'Show a customizable SweetAlert2 popup'
                    }),
                    arguments: {
                        title: {
                            type: ArgumentType.STRING,
                            defaultValue: 'Custom Title',
                        },
                        message: {
                            type: ArgumentType.STRING,
                            defaultValue: 'Custom Message',
                        },
                        icon: {
                            type: ArgumentType.DROPDOWN,
                            menu: 'iconMenu',
                            defaultValue: 'info',
                        },
                        confirmText: {
                            type: ArgumentType.STRING,
                            defaultValue: 'OK',
                        },
                    },
                },
                {
                    opcode: 'openUrlInNewTab',
                    blockType: BlockType.COMMAND,
                    text: formatMessage({
                        id: 'coreExample.openUrlInNewTab',
                        default: 'Open URL in New Tab: URL [url]',
                        description: 'Open a URL in a new tab'
                    }),
                    arguments: {
                        url: {
                            type: ArgumentType.STRING,
                            defaultValue: 'https://example.com',
                        },
                    },
                },
                {
                    opcode: 'buttonPressed',
                    blockType: BlockType.BOOLEAN,
                    text: formatMessage({
                        id: 'coreExample.buttonPressed',
                        default: 'Button Pressed',
                        description: 'Check if the button was pressed'
                    }),
                },
            ],
            menus: {
                iconMenu: {
                    acceptReporters: true,
                    items: [
                        { text: 'Info', value: 'info' },
                        { text: 'Success', value: 'success' },
                        { text: 'Warning', value: 'warning' },
                        { text: 'Error', value: 'error' },
                    ],
                },
            },
        };
    }

    showCustomSweetAlert(args) {
        const options = {
            title: args.title,
            text: args.message,
            icon: args.icon,
            confirmButtonText: args.confirmText,
        };

        Swal.fire(options);
    }

    openUrlInNewTab(args) {
        const url = args.url;
        window.open(url, '_blank');
    }

    buttonPressed() {
        return this.buttonPressed;
    }

    // cool
    onButtonDown() {
        this.buttonPressed = true;
    }

    // cool 2
    onButtonUp() {
        this.buttonPressed = false;
    }
}

module.exports = Sweetalert2ext;
