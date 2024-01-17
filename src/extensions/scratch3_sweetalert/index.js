const ArgumentType = require('../../extension-support/argument-type');
const BlockType = require('../../extension-support/block-type');
import Swal from 'sweetalert2';

class SweetAlert2Extension {
    constructor(runtime) {
        this.runtime = runtime;
    }

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
                {
                    opcode: 'playSound',
                    blockType: Scratch.BlockType.COMMAND,
                    text: 'play sound from URL [url]',
                    arguments: {
                        url: {
                            type: Scratch.ArgumentType.STRING,
                            defaultValue: 'https://example.com/sound.mp3',
                        },
                    },
                },
            ],
        };
    }

    async alert(args) {
        const { text, desc } = args;
        await this.showAlert(text, desc, false);
    }

    async alert2(args) {
        const { text, desc, url } = args;
        await this.showAlert(text, desc, true, url);
    }

    async playSound(args) {
        const { url } = args;
        await this.playSound(url);
    }

    async showAlert(text, desc, allowRedirect, url) {
        try {
            await Swal.fire({
                title: text,
                text: desc,
                confirmButtonText: 'Ok',
                icon: 'success',
                allowOutsideClick: allowRedirect,
                preConfirm: () => {
                    if (allowRedirect) {
                        window.location.href = url;
                    }
                },
            });
        } catch (error) {
            console.error('Error displaying SweetAlert2:', error);
        }
    }

    async playSound(url) {
        try {
            const audioEngine = this.runtime.audioEngine;
            const target = this.runtime.target;
            
            if (!(await this.runtime.canFetch(url))) {
                throw new Error(`Permission to fetch ${url} denied`);
            }

            const arrayBuffer = await this.fetchAsArrayBufferWithTimeout(url);
            const soundPlayer = await this.decodeSoundPlayer(arrayBuffer);
            const soundBank = target.sprite.soundBank;

            soundBank.addSoundPlayer(soundPlayer);
            await soundBank.playSound(target, soundPlayer.id);

            delete soundBank.soundPlayers[soundPlayer.id];
            soundBank.playerTargets.delete(soundPlayer.id);
            soundBank.soundEffects.delete(soundPlayer.id);
        } catch (e) {
            console.warn(`Failed to play sound from ${url}`, e);
        }
    }

    async fetchAsArrayBufferWithTimeout(url) {
        return new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest();
            const timeout = setTimeout(() => {
                xhr.abort();
                reject(new Error('Timed out'));
            }, 5000);
            xhr.onload = () => {
                clearTimeout(timeout);
                if (xhr.status === 200) {
                    resolve(xhr.response);
                } else {
                    reject(new Error(`HTTP error ${xhr.status} while fetching ${url}`));
                }
            };
            xhr.onerror = () => {
                clearTimeout(timeout);
                reject(new Error(`Failed to request ${url}`));
            };
            xhr.responseType = 'arraybuffer';
            xhr.open('GET', url);
            xhr.send();
        });
    }

    async decodeSoundPlayer(arrayBuffer) {
        return new Promise((resolve, reject) => {
            const audioEngine = this.runtime.audioEngine;
            audioEngine.decodeSoundPlayer({ data: { buffer: arrayBuffer } })
                .then((soundPlayer) => resolve(soundPlayer))
                .catch((error) => reject(error));
        });
    }
}

Scratch.extensions.register(new SweetAlert2Extension());
