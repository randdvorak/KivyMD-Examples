//
//  MDInterstitialViewController.m
//  interstitial
//
//  Created by Rand on 3/2/22.
//

#import "MDInterstitialViewController.h"

static GADInterstitialAd* currentAd = nil;

@class SDL_uikitwindow;

@interface MDInterstitialViewController () <GADFullScreenContentDelegate>
-(instancetype)initWithUnitID:(NSString*)unitID;
-(void)show_interstitial;
-(void)getNextAd;

@property(nonatomic, strong) GADInterstitialAd *interstitial;
@property(nonatomic, strong) NSString* adUnitID;

@end


@implementation MDInterstitialViewController

@synthesize fullScreenContentDelegate;

-(instancetype)initWithUnitID:(NSString*)unitID{
   self = [super init];
   if (self != nil)
   {
		self.adUnitID = unitID;
		[self getNextAd];
   }
   return self;
}
- (void)viewDidLoad {
    [super viewDidLoad];
}

-(void)getNextAd {
	GADRequest *request = [GADRequest request];
	[GADInterstitialAd loadWithAdUnitID:self.adUnitID
		 request:request
			completionHandler:^(GADInterstitialAd *_Nullable interstitialAd,
											   NSError *_Nullable error){
		if (error) {
		  NSLog(@"Failed to load interstitial ad with error: %@", [error localizedDescription]);
		  return;
		}
		interstitialAd.fullScreenContentDelegate = self;
		self.interstitial = interstitialAd;
	}];

}
-(void)show_interstitial{
	
		UIWindow * appWindow = [[UIApplication sharedApplication] delegate].window;
		UIViewController * rootViewController = appWindow.rootViewController;
		NSError* error = nil;
	BOOL canPresent = [self.interstitial canPresentFromRootViewController:rootViewController error:&error];
		if(canPresent){
			[self.interstitial presentFromRootViewController:rootViewController];
		}else{
			NSLog(@"Failed to present interstitial ad with error: %@", [error localizedDescription]);

		}
}
- (void)adWillPresentFullScreenContent:(id)ad {
  NSLog(@"Ad will present full screen content.");
}

- (void)ad:(id)ad didFailToPresentFullScreenContentWithError:(NSError *)error {
  NSLog(@"Ad failed to present full screen content with error %@.", [error localizedDescription]);
}

- (void)adDidDismissFullScreenContent:(id)ad {
  NSLog(@"Ad did dismiss full screen content.");
  [self getNextAd];
}

@end
