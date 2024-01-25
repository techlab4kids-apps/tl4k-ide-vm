const ArgumentType = require('../extension-support/argument-type');
const BlockType = require('../extension-support/block-type');
const formatMessage = require('format-message');
const Swal = require('sweetalert2');

class Sweetalert2ext {
    constructor(runtime) {
        this.runtime = runtime;
        this.buttonPressed = false;  // did you press it?
    }

    getInfo() {
        return {
            id: 'sweetalert2',
            name: 'Sweetalert2',
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
