"""
EchoLink CLI User Interface

This module provides an interactive command-line interface with rich colors,
navigation, and ADHD-friendly design elements.
"""

import sys
import time
import threading
import select
from typing import List, Callable, Optional, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.live import Live
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
import logging

from ..config.settings import settings


logger = logging.getLogger(__name__)


class CLIInterface:
    """Rich command-line interface for EchoLink"""
    
    def __init__(self):
        """Initialize the CLI interface"""
        self.console = Console(
            color_system="truecolor" if settings.cli_colors_enabled else "standard"
        )
        self.current_menu = "main"
        self.menu_stack: List[str] = []
        self.selected_index = 0
        self.running = False
        self.live_display = None
        
        # Menu definitions
        self.menus = {
            "main": {
                "title": "🎙️ EchoLink - Voice Interface for Cursor AI",
                "options": [
                    {"label": "🚀 Start Voice Monitoring", "action": "start_monitoring", "emoji": "🚀"},
                    {"label": "⚙️ Settings", "action": "settings_menu", "emoji": "⚙️"},
                    {"label": "🎤 Test Voice", "action": "test_voice", "emoji": "🎤"},
                    {"label": "📊 Status", "action": "show_status", "emoji": "📊"},
                    {"label": "❓ Help", "action": "show_help", "emoji": "❓"},
                    {"label": "↩️ Exit", "action": "exit", "emoji": "↩️"}
                ]
            },
            "settings": {
                "title": "⚙️ EchoLink Settings",
                "options": [
                    {"label": "🔊 Voice Settings", "action": "voice_settings", "emoji": "🔊"},
                    {"label": "📋 Monitor Settings", "action": "monitor_settings", "emoji": "📋"},
                    {"label": "🎨 UI Settings", "action": "ui_settings", "emoji": "🎨"},
                    {"label": "🔑 API Keys", "action": "api_settings", "emoji": "🔑"},
                    {"label": "↩️ Back", "action": "back", "emoji": "↩️"}
                ]
            },
            "voice_settings": {
                "title": "🔊 Voice Settings",
                "options": [
                    {"label": "🎭 Select Voice", "action": "select_voice", "emoji": "🎭"},
                    {"label": "🔊 Volume Control", "action": "volume_settings", "emoji": "🔊"},
                    {"label": "⚡ Speed Control", "action": "speed_settings", "emoji": "⚡"},
                    {"label": "↩️ Back", "action": "back", "emoji": "↩️"}
                ]
            }
        }
        
        # Status information
        self.status_data = {
            "monitoring": False,
            "api_connected": False,
            "last_processed": None,
            "processed_count": 0
        }
    
    def _create_header(self) -> Panel:
        """Create the header panel"""
        header_text = Text()
        header_text.append("EchoLink", style="bold blue")
        header_text.append(" - Voice Interface for Cursor AI", style="white")
        
        status_indicator = "🟢" if self.status_data["monitoring"] else "🔴"
        header_text.append(f" {status_indicator}", style="white")
        
        return Panel(
            header_text,
            title="[bold cyan]🎙️ EchoLink[/bold cyan]",
            border_style="blue",
            padding=(0, 1)
        )
    
    def _create_menu_panel(self, menu_name: str) -> Panel:
        """Create a menu panel with options
        
        Args:
            menu_name: Name of the menu to create
            
        Returns:
            Panel with menu options
        """
        menu_config = self.menus.get(menu_name, self.menus["main"])
        
        table = Table(show_header=False, show_lines=False, padding=(0, 2))
        table.add_column("", style="white", width=50)
        
        for i, option in enumerate(menu_config["options"]):
            if i == self.selected_index:
                # Highlighted option
                style = "bold white on blue"
                prefix = "▶ "
            else:
                style = "white"
                prefix = "  "
            
            table.add_row(f"{prefix}{option['emoji']} {option['label']}", style=style)
        
        return Panel(
            table,
            title=f"[bold green]{menu_config['title']}[/bold green]",
            border_style="green",
            padding=(1, 1)
        )
    
    def _create_status_panel(self) -> Panel:
        """Create the status information panel"""
        status_table = Table(show_header=False, show_lines=False)
        status_table.add_column("Label", style="cyan", width=20)
        status_table.add_column("Value", style="white", width=25)
        
        # Monitoring status
        monitor_status = "🟢 Active" if self.status_data["monitoring"] else "🔴 Inactive"
        status_table.add_row("Monitor:", monitor_status)
        
        # API status
        api_status = "🟢 Connected" if self.status_data["api_connected"] else "🔴 Disconnected"
        status_table.add_row("API:", api_status)
        
        # Processed count
        status_table.add_row("Processed:", f"📝 {self.status_data['processed_count']}")
        
        # Last activity
        if self.status_data["last_processed"]:
            last_time = self.status_data["last_processed"].strftime("%H:%M:%S")
            status_table.add_row("Last:", f"🕐 {last_time}")
        
        return Panel(
            status_table,
            title="[bold yellow]📊 Status[/bold yellow]",
            border_style="yellow",
            padding=(1, 1)
        )
    
    def _create_help_panel(self) -> Panel:
        """Create the help panel"""
        help_text = Text()
        help_text.append("Navigation:\n", style="bold cyan")
        help_text.append("Numbers (1-6): Select menu option\n", style="white")
        help_text.append("Enter: Select current option\n", style="white")
        help_text.append("B: Go back, Q: Quit\n", style="white")
        
        help_text.append("\nFeatures:\n", style="bold cyan")
        help_text.append("• Real-time clipboard monitoring\n", style="white")
        help_text.append("• Text summarization for voice\n", style="white")
        help_text.append("• ElevenLabs voice synthesis\n", style="white")
        help_text.append("• Configurable voice settings\n", style="white")
        
        return Panel(
            help_text,
            title="[bold magenta]❓ Help[/bold magenta]",
            border_style="magenta",
            padding=(1, 1)
        )
    
    def _create_layout(self) -> Layout:
        """Create the main layout"""
        layout = Layout()
        
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=4)
        )
        
        layout["body"].split_row(
            Layout(name="menu", ratio=2),
            Layout(name="sidebar", ratio=1)
        )
        
        # Populate layout
        layout["header"].update(self._create_header())
        layout["menu"].update(self._create_menu_panel(self.current_menu))
        layout["sidebar"].update(self._create_status_panel())
        
        # Create footer with input prompt
        footer_text = "[dim]Enter option number (1-6), 'b' for back, 'q' to quit:[/dim]\n"
        footer_text += f"[bold cyan]Choice: [/bold cyan]"
        
        layout["footer"].update(Panel(
            footer_text,
            border_style="dim"
        ))
        
        return layout
    
    def navigate_up(self):
        """Navigate up in the current menu"""
        current_options = self.menus.get(self.current_menu, self.menus["main"])["options"]
        self.selected_index = (self.selected_index - 1) % len(current_options)
    
    def navigate_down(self):
        """Navigate down in the current menu"""
        current_options = self.menus.get(self.current_menu, self.menus["main"])["options"]
        self.selected_index = (self.selected_index + 1) % len(current_options)
    
    def select_option(self) -> Optional[str]:
        """Select the current option and return the action"""
        current_options = self.menus.get(self.current_menu, self.menus["main"])["options"]
        if 0 <= self.selected_index < len(current_options):
            return current_options[self.selected_index]["action"]
        return None
    
    def change_menu(self, menu_name: str):
        """Change to a different menu"""
        if menu_name != "back":
            self.menu_stack.append(self.current_menu)
        
        if menu_name == "back" and self.menu_stack:
            self.current_menu = self.menu_stack.pop()
        else:
            self.current_menu = menu_name
        
        self.selected_index = 0
    
    def show_message(self, message: str, title: str = "Message", style: str = "info"):
        """Show a temporary message to the user
        
        Args:
            message: Message to display
            title: Title for the message panel
            style: Style type (info, success, warning, error)
        """
        style_map = {
            "info": ("blue", "ℹ️"),
            "success": ("green", "✅"),
            "warning": ("yellow", "⚠️"),
            "error": ("red", "❌")
        }
        
        border_style, emoji = style_map.get(style, style_map["info"])
        
        panel = Panel(
            Text(message, style="white"),
            title=f"[bold {border_style}]{emoji} {title}[/bold {border_style}]",
            border_style=border_style,
            padding=(1, 2)
        )
        
        self.console.print(panel)
        input("\nPress Enter to continue...")
    
    def show_progress(self, task_name: str, duration: float = 2.0):
        """Show a progress indicator
        
        Args:
            task_name: Name of the task
            duration: Duration to show progress
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task(f"🔄 {task_name}...", total=None)
            time.sleep(duration)
            progress.update(task, description=f"✅ {task_name} complete!")
            time.sleep(0.5)
    
    def get_text_input(self, prompt: str) -> str:
        """Get text input from user
        
        Args:
            prompt: Prompt to display
            
        Returns:
            User input string
        """
        return Prompt.ask(f"[cyan]{prompt}[/cyan]")
    
    def confirm_action(self, message: str) -> bool:
        """Ask user to confirm an action
        
        Args:
            message: Confirmation message
            
        Returns:
            True if confirmed, False otherwise
        """
        response = Prompt.ask(
            f"[yellow]❓ {message}[/yellow]",
            choices=["y", "n", "yes", "no"],
            default="n"
        )
        return response.lower() in ['y', 'yes']
    
    def update_status(self, **kwargs):
        """Update status information
        
        Args:
            **kwargs: Status fields to update
        """
        self.status_data.update(kwargs)
    
    def clear_screen(self):
        """Clear the console screen"""
        self.console.clear()
    
    def display_menu_and_get_choice(self) -> str:
        """Display menu and get user choice"""
        self.console.clear()
        
        # Show the layout
        layout = self._create_layout()
        self.console.print(layout)
        
        # Get user input
        current_options = self.menus.get(self.current_menu, self.menus["main"])["options"]
        max_option = len(current_options)
        
        while True:
            try:
                choice = input().strip().lower()
                
                if choice == 'q':
                    return 'exit'
                elif choice == 'b':
                    return 'back'
                elif choice.isdigit():
                    option_num = int(choice)
                    if 1 <= option_num <= max_option:
                        self.selected_index = option_num - 1
                        action = self.select_option()
                        return action if action else 'exit'
                    else:
                        self.console.print(f"[red]Please enter a number between 1 and {max_option}[/red]")
                elif choice == '':
                    # Enter pressed, select current option
                    action = self.select_option()
                    return action if action else 'exit'
                else:
                    self.console.print(f"[red]Invalid choice. Enter 1-{max_option}, 'b' for back, or 'q' to quit.[/red]")
            except (ValueError, KeyboardInterrupt):
                return 'exit'
    
    def run_interface(self, action_handler: Callable[[str], bool]):
        """Run the main interface loop
        
        Args:
            action_handler: Function to handle menu actions
        """
        self.running = True
        
        try:
            self.console.print("[bold green]🎙️ Welcome to EchoLink![/bold green]")
            self.console.print("[dim]Configure your API keys in .env file for full functionality.[/dim]\n")
            
            while self.running:
                # Display menu and get choice
                action = self.display_menu_and_get_choice()
                
                if action == "exit":
                    break
                elif action == "back":
                    if self.menu_stack:
                        self.change_menu("back")
                    else:
                        # Already at main menu, ask to exit
                        if self.confirm_action("Exit EchoLink?"):
                            break
                elif action:
                    # Handle the action
                    should_continue = action_handler(action)
                    if not should_continue:
                        break
                
        except KeyboardInterrupt:
            self.running = False
        finally:
            self.running = False
            self.console.print("\n[dim]Goodbye! 👋[/dim]") 