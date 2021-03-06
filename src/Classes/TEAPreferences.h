//
//  TEAPreferences.h
//  TEA for Espresso.sugar
//
//  Created by Ian Beck
//  http://onecrayon.com/tea/
//
//  MIT License
//

#import <Cocoa/Cocoa.h>

// ==========================================================

// The class that allows us to change nil to an empty string

@interface TEANilToString : NSValueTransformer {
	
}

+ (Class)transformedValueClass;
+ (BOOL)allowsReverseTransformation;

- (NSString *)transformedValue:(id)value;
- (NSString *)reverseTransformedValue:(id)value;

@end


@interface TEAPreferencesViewController : NSViewController
{
	NSArrayController *arrayController;
	NSTableView *tableView;
	NSTextField *versionInfo;
}

@property (readonly,retain) IBOutlet NSArrayController *arrayController;
@property (readonly,retain) IBOutlet NSTableView *tableView;
@property (readonly,retain) IBOutlet NSTextField *versionInfo;

- (IBAction)addListItem:(id)sender;
- (IBAction)toggleUserActions:(id)sender;
- (IBAction)customActionsHelp:(id)sender;

@end
