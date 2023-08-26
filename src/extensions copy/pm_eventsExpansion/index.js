const BlockType = require('../../extension-support/block-type');
const ArgumentType = require('../../extension-support/argument-type');
const Cast = require('../../util/cast');

const blockSeparator = '<sep gap="36"/>'; // At default scale, about 28px

const blocks = `
<!-- %b4 > nah -->
<block type="event_whenbroadcastreceived"></block>
<block type="pmEventsExpansion_sendWithData">
    <value name="BROADCAST">
        <shadow type="event_broadcast_menu"></shadow>
    </value>
    <value name="DATA">
        <shadow type="text">
            <field name="TEXT">abc</field>
        </shadow>
    </value>
</block>
%b5>
${blockSeparator}
<!-- %b6 > -->
<block type="pmEventsExpansion_broadcastToSprite">
    <value name="BROADCAST">
        <shadow type="event_broadcast_menu"></shadow>
    </value>
</block>
<block type="pmEventsExpansion_broadcastFunction">
    <value name="BROADCAST">
        <shadow type="event_broadcast_menu"></shadow>
    </value>
</block>
%b8>
${blockSeparator}
%b2>
%b0>
%b1>
<block type="pmEventsExpansion_broadcastThreadCount">
    <value name="BROADCAST">
        <shadow type="event_broadcast_menu"></shadow>
    </value>
</block>
`

/**
 * Class of idk
 * @constructor
 */
class pmEventsExpansion {
    constructor(runtime) {
        /**
         * The runtime instantiating this block package.
         * @type {runtime}
         */
        this.runtime = runtime;
        // every other frame block
        this._otherFrame = false;
        this.runtime.on('RUNTIME_STEP_START', () => {
            this._everyOtherFrame();
        });
    }

    // stepUpdates
    _everyOtherFrame() {
        if (this._otherFrame) {
            this.runtime.startHats('pmEventsExpansion_everyOtherFrame');
            this._otherFrame = false;
        } else {
            this._otherFrame = true;
        }
    }

    // order
    orderCategoryBlocks(extensionBlocks) {
        let categoryBlocks = blocks;

        let idx = 0;
        for (const block of extensionBlocks) {
            categoryBlocks = categoryBlocks.replace('%b' + idx + '>', block);
            idx++;
        }

        return [categoryBlocks];
    }

    /**
     * @returns {object} metadata for extension
     */
    getInfo() {
        return {
            id: 'pmEventsExpansion',
            name: 'Events Expansion',
            color1: '#FFBF00',
            color2: '#E6AC00',
            color3: '#CC9900',
            isDynamic: true,
            orderBlocks: this.orderCategoryBlocks,
            blocks: [
                {
                    opcode: 'everyOtherFrame',
                    text: 'every other frame',
                    blockType: BlockType.HAT,
                    isEdgeActivated: false
                },
                {
                    opcode: 'neverr',
                    text: 'never',
                    blockType: BlockType.HAT,
                    isEdgeActivated: false
                },
                {
                    opcode: 'whenSpriteClicked',
                    text: 'when [SPRITE] clicked',
                    blockType: BlockType.HAT,
                    isEdgeActivated: false,
                    arguments: {
                        SPRITE: {
                            type: ArgumentType.STRING,
                            menu: "spriteId"
                        }
                    }
                },
                {
                    opcode: 'sendWithData',
                    text: 'broadcast [BROADCAST] with data [DATA]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        BROADCAST: {
                            type: ArgumentType.STRING,
                            defaultValue: "your not supposed to see this?"
                        },
                        DATA: {
                            type: ArgumentType.STRING,
                            defaultValue: "abc"
                        }
                    }
                },
                {
                    opcode: 'receivedData',
                    text: 'when I receive [BROADCAST] with data',
                    blockType: BlockType.HAT,
                    isEdgeActivated: false,
                    arguments: {
                        BROADCAST: {
                            type: ArgumentType.STRING,
                            menu: "broadcastMenu"
                        }
                    }
                },
                {
                    opcode: 'recievedDataReporter',
                    text: 'recieved data',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true
                },
                {
                    opcode: 'broadcastToSprite',
                    text: 'broadcast [BROADCAST] to [SPRITE]',
                    blockType: BlockType.COMMAND,
                    arguments: {
                        BROADCAST: {
                            type: ArgumentType.STRING,
                            defaultValue: "your not supposed to see this?"
                        },
                        SPRITE: {
                            type: ArgumentType.STRING,
                            menu: "spriteId"
                        }
                    }
                },
                {
                    opcode: 'broadcastFunction',
                    text: 'broadcast [BROADCAST] and wait',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true,
                    arguments: {
                        BROADCAST: {
                            type: ArgumentType.STRING,
                            defaultValue: "your not supposed to see this?"
                        }
                    }
                },
                {
                    opcode: 'returnFromBroadcastFunc',
                    text: 'return [VALUE]',
                    blockType: BlockType.COMMAND,
                    isTerminal: true,
                    disableMonitor: true,
                    arguments: {
                        VALUE: {
                            type: ArgumentType.STRING,
                            defaultValue: "1"
                        }
                    }
                },
                {
                    opcode: 'broadcastThreadCount',
                    text: 'broadcast [BROADCAST] and get # of blocks started',
                    blockType: BlockType.REPORTER,
                    disableMonitor: true
                },
            ],
            menus: {
                spriteId: "_spriteId",
                broadcastMenu: "_broadcastMenu"
            }
        };
    }

    // menus
    _spriteId() {
        const emptyMenu = [{ text: '', value: '' }];
        const menu = [];
        for (const target of this.runtime.targets) {
            if (target.isStage) {
                menu.push({
                    text: "stage",
                    value: target.id
                });
                continue;
            }
            menu.push({
                text: target.sprite.name,
                value: target.id
            });
        }
        if (menu.length <= 0) return emptyMenu;
        return menu;
    }
    _broadcastMenu() {
        const emptyMenu = [{ text: '', value: '' }];
        const menu = [];
        for (const target of this.runtime.targets) {
            if (target.isStage) {
                menu.push({
                    text: "stage",
                    value: target.id
                });
                continue;
            }
            menu.push({
                text: target.sprite.name,
                value: target.id
            });
        }
        if (menu.length <= 0) return emptyMenu;
        return menu;
    }

    // blocks
    sendWithData(args, util) {
        const broadcast = Cast.toString(args.BROADCAST);
        const data = Cast.toString(args.DATA);
        const threads = util.startHats("event_whenbroadcastreceived", {
            BROADCAST_OPTION: broadcast
        });
        for (const thread of threads) {
            thread.__evex_recievedDataa = data;
        }
    }
    broadcastToSprite(args, util) {
        const broadcast = Cast.toString(args.BROADCAST);
        const sprite = Cast.toString(args.SPRITE);
        const target = this.runtime.getTargetById(sprite);
        util.startHats("event_whenbroadcastreceived", {
            BROADCAST_OPTION: broadcast
        }, target);
    }
    broadcastThreadCount(args, util) {
        const broadcast = Cast.toString(args.BROADCAST);
        const threads = util.startHats("event_whenbroadcastreceived", {
            BROADCAST_OPTION: broadcast
        });
        return threads.length;
    }
    recievedDataReporter(_, util) {
        return util.thread.__evex_recievedDataa;
    }
    returnFromBroadcastFunc(args, util) {
        util.thread.__evex_returnDataa = args.VALUE;
    }
}

module.exports = pmEventsExpansion;
